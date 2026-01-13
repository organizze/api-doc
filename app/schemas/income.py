from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class IncomeStatus(str, Enum):
    PENDING = "pending"
    RECEIVED = "received"
    PARTIAL = "partial"
    OVERDUE = "overdue"


# === Recebimentos Previstos (do PDF/manual) ===


class ExpectedIncomeCreate(BaseModel):
    client_name: str = Field(..., max_length=255)
    description: Optional[str] = None
    expected_amount_cents: int = Field(..., gt=0)
    expected_date: date
    category_id: Optional[int] = None
    account_id: Optional[int] = None
    reference_month: int = Field(..., ge=1, le=12)
    reference_year: int = Field(..., ge=2020)


class ExpectedIncomeUpdate(BaseModel):
    client_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    expected_amount_cents: Optional[int] = Field(None, gt=0)
    expected_date: Optional[date] = None
    status: Optional[IncomeStatus] = None
    actual_amount_cents: Optional[int] = None
    actual_date: Optional[date] = None
    organizze_transaction_id: Optional[int] = None


class ExpectedIncomeResponse(BaseModel):
    id: str
    source_document: Optional[str] = None
    client_name: str
    description: Optional[str] = None
    expected_amount_cents: int
    expected_date: date
    actual_amount_cents: int = 0
    actual_date: Optional[date] = None
    status: IncomeStatus
    organizze_transaction_id: Optional[int] = None
    category_id: Optional[int] = None
    account_id: Optional[int] = None
    reference_month: int
    reference_year: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Computed
    @property
    def difference_cents(self) -> int:
        return self.actual_amount_cents - self.expected_amount_cents


# === Recebimentos Reais (do Organizze) ===


class ActualIncomeResponse(BaseModel):
    id: int  # transaction_id do Organizze
    description: str
    date: date
    amount_cents: int
    category_id: Optional[int] = None
    account_id: int
    paid: bool


# === Comparação ===


class IncomeComparisonResponse(BaseModel):
    month: int
    year: int

    # Totais
    total_expected_cents: int
    total_actual_cents: int
    difference_cents: int

    # Detalhes
    reconciled: List[ExpectedIncomeResponse]
    pending: List[ExpectedIncomeResponse]
    extras: List[ActualIncomeResponse]
