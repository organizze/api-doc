from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date

from app.database import supabase
from app.schemas.expenses import (
    BudgetCreate,
    BudgetUpdate,
    BudgetResponse,
    ActualExpenseResponse,
    ExpenseByCategoryResponse,
    ExpenseComparisonResponse,
)
from app.services.organizze_client import organizze_client

router = APIRouter(prefix="/expenses", tags=["Despesas"])


# === ORÇAMENTO (GASTOS PREVISTOS) ===


@router.get("/budget", response_model=List[BudgetResponse])
async def list_budgets(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020),
):
    """
    Lista orçamentos planejados por categoria para o mês/ano.
    Inclui valor gasto atual do Organizze.
    """
    # Buscar budgets do Supabase
    response = (
        supabase.table("budgets")
        .select("*")
        .eq("month", month)
        .eq("year", year)
        .execute()
    )
    budgets = response.data

    # Buscar gastos reais do Organizze
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    transactions = await organizze_client.get_transactions(
        start_date=start_date,
        end_date=end_date,
    )

    # Agrupar despesas por categoria
    expenses_by_category = {}
    for t in transactions:
        if t.get("amount_cents", 0) < 0:  # Apenas despesas
            cat_id = t.get("category_id")
            if cat_id:
                expenses_by_category[cat_id] = expenses_by_category.get(cat_id, 0) + abs(
                    t["amount_cents"]
                )

    # Enriquecer budgets com dados reais
    results = []
    for budget in budgets:
        cat_id = budget["organizze_category_id"]
        actual = expenses_by_category.get(cat_id, 0)
        planned = budget["planned_amount_cents"]
        percentage = (actual / planned * 100) if planned > 0 else 0

        results.append(
            BudgetResponse(
                **budget,
                actual_amount_cents=actual,
                percentage_used=round(percentage, 2),
                is_over_budget=actual > planned,
                is_alert=percentage >= budget["alert_threshold"],
            )
        )

    return results


@router.post("/budget", response_model=BudgetResponse)
async def create_budget(data: BudgetCreate):
    """Cria um orçamento para uma categoria."""
    # Verificar se já existe budget para esta categoria/período
    existing = (
        supabase.table("budgets")
        .select("id")
        .eq("organizze_category_id", data.organizze_category_id)
        .eq("month", data.month)
        .eq("year", data.year)
        .execute()
    )

    if existing.data:
        raise HTTPException(
            400, "Já existe um orçamento para esta categoria neste período"
        )

    response = supabase.table("budgets").insert(data.model_dump()).execute()
    if not response.data:
        raise HTTPException(500, "Erro ao criar orçamento")

    return BudgetResponse(**response.data[0])


@router.put("/budget/{budget_id}", response_model=BudgetResponse)
async def update_budget(budget_id: str, data: BudgetUpdate):
    """Atualiza um orçamento"""
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}

    response = (
        supabase.table("budgets").update(update_data).eq("id", budget_id).execute()
    )
    if not response.data:
        raise HTTPException(404, "Orçamento não encontrado")

    return BudgetResponse(**response.data[0])


@router.delete("/budget/{budget_id}")
async def delete_budget(budget_id: str):
    """Remove um orçamento"""
    supabase.table("budgets").delete().eq("id", budget_id).execute()
    return {"deleted": True, "id": budget_id}


@router.post("/budget/copy")
async def copy_budgets_to_next_month(
    source_month: int = Query(..., ge=1, le=12),
    source_year: int = Query(..., ge=2020),
):
    """Copia todos os orçamentos de um mês para o próximo."""
    # Buscar budgets do mês fonte
    response = (
        supabase.table("budgets")
        .select("*")
        .eq("month", source_month)
        .eq("year", source_year)
        .execute()
    )

    if not response.data:
        raise HTTPException(404, "Nenhum orçamento encontrado no mês fonte")

    # Calcular próximo mês
    if source_month == 12:
        target_month = 1
        target_year = source_year + 1
    else:
        target_month = source_month + 1
        target_year = source_year

    # Copiar budgets
    copied = []
    for budget in response.data:
        new_budget = {
            "organizze_category_id": budget["organizze_category_id"],
            "category_name": budget.get("category_name"),
            "month": target_month,
            "year": target_year,
            "planned_amount_cents": budget["planned_amount_cents"],
            "is_recurring": budget.get("is_recurring", False),
            "alert_threshold": budget.get("alert_threshold", 80),
        }

        # Verificar se já existe
        existing = (
            supabase.table("budgets")
            .select("id")
            .eq("organizze_category_id", new_budget["organizze_category_id"])
            .eq("month", target_month)
            .eq("year", target_year)
            .execute()
        )

        if not existing.data:
            result = supabase.table("budgets").insert(new_budget).execute()
            if result.data:
                copied.append(result.data[0])

    return {
        "copied_count": len(copied),
        "target_month": target_month,
        "target_year": target_year,
        "budgets": copied,
    }


# === GASTOS REAIS (do Organizze) ===


@router.get("/actual", response_model=List[ActualExpenseResponse])
async def get_actual_expenses(
    start_date: date = Query(...),
    end_date: date = Query(...),
    category_id: Optional[int] = Query(None),
    account_id: Optional[int] = Query(None),
):
    """
    Busca despesas reais da API do Organizze.
    Filtra transações com amount_cents < 0 (despesas).
    """
    transactions = await organizze_client.get_transactions(
        start_date=start_date,
        end_date=end_date,
        account_id=account_id,
    )

    # Filtrar despesas
    expenses = [t for t in transactions if t.get("amount_cents", 0) < 0]

    if category_id:
        expenses = [e for e in expenses if e.get("category_id") == category_id]

    return [
        ActualExpenseResponse(
            id=t["id"],
            description=t.get("description", ""),
            date=t["date"],
            amount_cents=t["amount_cents"],
            category_id=t.get("category_id"),
            account_id=t["account_id"],
            paid=t.get("paid", False),
        )
        for t in expenses
    ]


@router.get("/by-category", response_model=List[ExpenseByCategoryResponse])
async def get_expenses_by_category(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020),
):
    """Retorna gastos agrupados por categoria."""
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    transactions = await organizze_client.get_transactions(
        start_date=start_date,
        end_date=end_date,
    )

    # Buscar categorias
    categories = await organizze_client.get_categories()
    category_names = {c["id"]: c["name"] for c in categories}

    # Buscar budgets
    budgets_response = (
        supabase.table("budgets")
        .select("*")
        .eq("month", month)
        .eq("year", year)
        .execute()
    )
    budgets = {b["organizze_category_id"]: b["planned_amount_cents"] for b in budgets_response.data}

    # Agrupar despesas por categoria
    grouped = {}
    for t in transactions:
        if t.get("amount_cents", 0) < 0:
            cat_id = t.get("category_id")
            if cat_id:
                if cat_id not in grouped:
                    grouped[cat_id] = {"total": 0, "count": 0}
                grouped[cat_id]["total"] += abs(t["amount_cents"])
                grouped[cat_id]["count"] += 1

    results = []
    for cat_id, data in grouped.items():
        budget_cents = budgets.get(cat_id)
        percentage = None
        if budget_cents:
            percentage = round(data["total"] / budget_cents * 100, 2)

        results.append(
            ExpenseByCategoryResponse(
                category_id=cat_id,
                category_name=category_names.get(cat_id, "Desconhecida"),
                total_cents=data["total"],
                transaction_count=data["count"],
                budget_cents=budget_cents,
                percentage_of_budget=percentage,
            )
        )

    return sorted(results, key=lambda x: x.total_cents, reverse=True)


# === COMPARAÇÃO ===


@router.get("/comparison", response_model=ExpenseComparisonResponse)
async def compare_expenses(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020),
):
    """Compara orçamento vs gastos reais por categoria."""
    # Buscar budgets e gastos por categoria
    budgets = await list_budgets(month=month, year=year)
    categories_data = await get_expenses_by_category(month=month, year=year)

    total_budgeted = sum(b.planned_amount_cents for b in budgets)
    total_actual = sum(c.total_cents for c in categories_data)

    # Gerar alertas
    alerts = []
    for budget in budgets:
        if budget.is_over_budget:
            alerts.append(
                f"Categoria '{budget.category_name}' estourou o orçamento: "
                f"{budget.percentage_used:.1f}% usado"
            )
        elif budget.is_alert:
            alerts.append(
                f"Categoria '{budget.category_name}' próxima do limite: "
                f"{budget.percentage_used:.1f}% usado"
            )

    return ExpenseComparisonResponse(
        month=month,
        year=year,
        total_budgeted_cents=total_budgeted,
        total_actual_cents=total_actual,
        difference_cents=total_budgeted - total_actual,
        categories=categories_data,
        alerts=alerts,
    )
