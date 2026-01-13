from pydantic import BaseModel
from typing import List, Optional


class DashboardSummary(BaseModel):
    # Recebimentos
    expected_income_cents: int
    actual_income_cents: int
    income_difference_cents: int
    income_percentage: float

    # Despesas
    budgeted_expenses_cents: int
    actual_expenses_cents: int
    expense_difference_cents: int
    expense_percentage: float

    # Saldo
    net_expected_cents: int
    net_actual_cents: int

    # Investimentos
    total_invested_cents: int
    investment_profit_cents: int


class CategoryDetail(BaseModel):
    category_id: Optional[int]
    category_name: str
    planned_cents: int
    actual_cents: int
    difference_cents: int
    percentage: float


class DashboardResponse(BaseModel):
    month: int
    year: int
    summary: DashboardSummary
    income_details: List[CategoryDetail]
    expense_details: List[CategoryDetail]
    alerts: List[str]
