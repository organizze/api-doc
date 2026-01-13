from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


# === Orçamento (Gastos Previstos) ===


class BudgetCreate(BaseModel):
    organizze_category_id: int
    category_name: Optional[str] = None
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2020)
    planned_amount_cents: int = Field(..., gt=0)
    is_recurring: bool = False
    alert_threshold: int = Field(default=80, ge=0, le=100)


class BudgetUpdate(BaseModel):
    planned_amount_cents: Optional[int] = Field(None, gt=0)
    is_recurring: Optional[bool] = None
    alert_threshold: Optional[int] = Field(None, ge=0, le=100)


class BudgetResponse(BaseModel):
    id: str
    organizze_category_id: int
    category_name: Optional[str] = None
    month: int
    year: int
    planned_amount_cents: int
    is_recurring: bool
    alert_threshold: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Valores calculados (preenchidos pelo service)
    actual_amount_cents: int = 0
    percentage_used: float = 0.0
    is_over_budget: bool = False
    is_alert: bool = False


# === Despesas Reais (do Organizze) ===


class ActualExpenseResponse(BaseModel):
    id: int
    description: str
    date: date
    amount_cents: int  # Valor negativo (despesa)
    category_id: Optional[int] = None
    account_id: int
    paid: bool


class ExpenseByCategoryResponse(BaseModel):
    category_id: int
    category_name: str
    total_cents: int
    transaction_count: int
    budget_cents: Optional[int] = None
    percentage_of_budget: Optional[float] = None


# === Comparação ===


class ExpenseComparisonResponse(BaseModel):
    month: int
    year: int

    # Totais
    total_budgeted_cents: int
    total_actual_cents: int
    difference_cents: int

    # Por categoria
    categories: List[ExpenseByCategoryResponse]

    # Alertas
    alerts: List[str]
