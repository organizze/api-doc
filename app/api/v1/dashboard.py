from fastapi import APIRouter, Query
from datetime import date

from app.database import supabase
from app.schemas.dashboard import (
    DashboardResponse,
    DashboardSummary,
    CategoryDetail,
)
from app.services.organizze_client import organizze_client

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
async def get_dashboard(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020),
):
    """
    Retorna visão consolidada do dashboard financeiro:
    - Recebimentos previstos vs realizados
    - Gastos previstos (budget) vs realizados
    - Saldo das contas
    - Resumo de investimentos
    """
    # Definir período
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    # === RECEBIMENTOS ===
    # Previstos (Supabase)
    expected_income_response = (
        supabase.table("expected_incomes")
        .select("*")
        .eq("reference_month", month)
        .eq("reference_year", year)
        .execute()
    )
    expected_incomes = expected_income_response.data
    total_expected_income = sum(
        e["expected_amount_cents"] for e in expected_incomes
    )

    # Reais (Organizze)
    transactions = await organizze_client.get_transactions(
        start_date=start_date,
        end_date=end_date,
    )
    actual_incomes = [t for t in transactions if t.get("amount_cents", 0) > 0]
    total_actual_income = sum(t["amount_cents"] for t in actual_incomes)

    # === DESPESAS ===
    # Orçamento (Supabase)
    budgets_response = (
        supabase.table("budgets")
        .select("*")
        .eq("month", month)
        .eq("year", year)
        .execute()
    )
    budgets = budgets_response.data
    total_budgeted = sum(b["planned_amount_cents"] for b in budgets)

    # Reais (Organizze)
    actual_expenses = [t for t in transactions if t.get("amount_cents", 0) < 0]
    total_actual_expenses = sum(abs(t["amount_cents"]) for t in actual_expenses)

    # === INVESTIMENTOS ===
    investments_response = (
        supabase.table("investments").select("*").eq("is_active", True).execute()
    )
    investments = investments_response.data
    total_invested = sum(i["initial_amount_cents"] for i in investments)
    total_current = sum(i["current_amount_cents"] for i in investments)
    investment_profit = total_current - total_invested

    # === DETALHES POR CATEGORIA ===
    # Buscar categorias
    categories = await organizze_client.get_categories()
    category_names = {c["id"]: c["name"] for c in categories}

    # Agrupar receitas por categoria
    income_by_category = {}
    for t in actual_incomes:
        cat_id = t.get("category_id")
        if cat_id:
            income_by_category[cat_id] = income_by_category.get(cat_id, 0) + t[
                "amount_cents"
            ]

    # Agrupar despesas por categoria
    expenses_by_category = {}
    for t in actual_expenses:
        cat_id = t.get("category_id")
        if cat_id:
            expenses_by_category[cat_id] = expenses_by_category.get(cat_id, 0) + abs(
                t["amount_cents"]
            )

    # Criar detalhes de receita
    income_details = []
    for cat_id, actual in income_by_category.items():
        income_details.append(
            CategoryDetail(
                category_id=cat_id,
                category_name=category_names.get(cat_id, "Desconhecida"),
                planned_cents=0,  # Não temos previsão por categoria para receitas
                actual_cents=actual,
                difference_cents=actual,
                percentage=100.0,
            )
        )

    # Criar detalhes de despesa
    expense_details = []
    budget_by_category = {b["organizze_category_id"]: b for b in budgets}

    for cat_id, actual in expenses_by_category.items():
        budget = budget_by_category.get(cat_id)
        planned = budget["planned_amount_cents"] if budget else 0
        percentage = (actual / planned * 100) if planned > 0 else 0

        expense_details.append(
            CategoryDetail(
                category_id=cat_id,
                category_name=category_names.get(cat_id, "Desconhecida"),
                planned_cents=planned,
                actual_cents=actual,
                difference_cents=planned - actual,
                percentage=round(percentage, 2),
            )
        )

    # === ALERTAS ===
    alerts = []
    for detail in expense_details:
        if detail.percentage > 100:
            alerts.append(
                f"Categoria '{detail.category_name}' estourou o orçamento: "
                f"{detail.percentage:.1f}% usado"
            )
        elif detail.percentage >= 80:
            alerts.append(
                f"Categoria '{detail.category_name}' próxima do limite: "
                f"{detail.percentage:.1f}% usado"
            )

    # Alertas de receita
    if total_actual_income < total_expected_income * 0.8:
        alerts.append(
            f"Receita abaixo do esperado: {total_actual_income/100:.2f} de "
            f"{total_expected_income/100:.2f} esperados"
        )

    # === MONTAR RESPOSTA ===
    income_percentage = (
        (total_actual_income / total_expected_income * 100)
        if total_expected_income > 0
        else 0
    )
    expense_percentage = (
        (total_actual_expenses / total_budgeted * 100) if total_budgeted > 0 else 0
    )

    summary = DashboardSummary(
        expected_income_cents=total_expected_income,
        actual_income_cents=total_actual_income,
        income_difference_cents=total_actual_income - total_expected_income,
        income_percentage=round(income_percentage, 2),
        budgeted_expenses_cents=total_budgeted,
        actual_expenses_cents=total_actual_expenses,
        expense_difference_cents=total_budgeted - total_actual_expenses,
        expense_percentage=round(expense_percentage, 2),
        net_expected_cents=total_expected_income - total_budgeted,
        net_actual_cents=total_actual_income - total_actual_expenses,
        total_invested_cents=total_current,
        investment_profit_cents=investment_profit,
    )

    return DashboardResponse(
        month=month,
        year=year,
        summary=summary,
        income_details=sorted(income_details, key=lambda x: x.actual_cents, reverse=True),
        expense_details=sorted(expense_details, key=lambda x: x.actual_cents, reverse=True),
        alerts=alerts,
    )
