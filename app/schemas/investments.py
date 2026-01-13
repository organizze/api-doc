from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class InvestmentType(str, Enum):
    FIXED_INCOME = "fixed_income"  # Renda Fixa (CDB, LCI, LCA, Tesouro)
    STOCKS = "stocks"  # Ações
    REITS = "reits"  # FIIs
    CRYPTO = "crypto"  # Criptomoedas
    SAVINGS = "savings"  # Poupança
    INVESTMENT_FUND = "investment_fund"  # Fundos de investimento
    OTHER = "other"


class InvestmentCreate(BaseModel):
    name: str = Field(..., max_length=255)
    ticker: Optional[str] = Field(None, max_length=20)
    type: InvestmentType
    institution: Optional[str] = Field(None, max_length=255)
    initial_amount_cents: int = Field(..., gt=0)
    current_amount_cents: int = Field(..., gt=0)
    purchase_date: date
    maturity_date: Optional[date] = None
    yield_rate: Optional[float] = None
    yield_type: Optional[str] = Field(None, max_length=50)
    organizze_account_id: Optional[int] = None
    notes: Optional[str] = None


class InvestmentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    ticker: Optional[str] = Field(None, max_length=20)
    type: Optional[InvestmentType] = None
    institution: Optional[str] = Field(None, max_length=255)
    current_amount_cents: Optional[int] = Field(None, gt=0)
    maturity_date: Optional[date] = None
    yield_rate: Optional[float] = None
    yield_type: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class InvestmentResponse(BaseModel):
    id: str
    name: str
    ticker: Optional[str] = None
    type: InvestmentType
    institution: Optional[str] = None
    initial_amount_cents: int
    current_amount_cents: int
    purchase_date: date
    maturity_date: Optional[date] = None
    yield_rate: Optional[float] = None
    yield_type: Optional[str] = None
    organizze_account_id: Optional[int] = None
    notes: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Calculados
    @property
    def profit_cents(self) -> int:
        return self.current_amount_cents - self.initial_amount_cents

    @property
    def profit_percentage(self) -> float:
        if self.initial_amount_cents == 0:
            return 0.0
        return (self.profit_cents / self.initial_amount_cents) * 100


class InvestmentHistoryResponse(BaseModel):
    id: str
    investment_id: str
    amount_cents: int
    recorded_at: datetime
    source: str


class InvestmentSummaryResponse(BaseModel):
    total_invested_cents: int
    total_current_cents: int
    total_profit_cents: int
    profit_percentage: float

    by_type: List[dict]  # [{type, total_cents, count}]
    by_institution: List[dict]  # [{institution, total_cents, count}]
