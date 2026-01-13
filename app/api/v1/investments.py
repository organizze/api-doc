from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from app.database import supabase
from app.schemas.investments import (
    InvestmentType,
    InvestmentCreate,
    InvestmentUpdate,
    InvestmentResponse,
    InvestmentHistoryResponse,
    InvestmentSummaryResponse,
)

router = APIRouter(prefix="/investments", tags=["Investimentos"])


@router.get("/", response_model=List[InvestmentResponse])
async def list_investments(
    type: Optional[InvestmentType] = Query(None),
    is_active: bool = Query(True),
):
    """
    Lista todos os investimentos.
    Pode filtrar por tipo e status ativo.
    """
    query = supabase.table("investments").select("*").eq("is_active", is_active)

    if type:
        query = query.eq("type", type.value)

    response = query.order("name").execute()
    return response.data


@router.get("/summary", response_model=InvestmentSummaryResponse)
async def get_investment_summary():
    """
    Resumo consolidado dos investimentos:
    - Total investido
    - Valor atual
    - Rendimento total
    - Distribuição por tipo
    """
    response = (
        supabase.table("investments").select("*").eq("is_active", True).execute()
    )
    investments = response.data

    total_invested = sum(i["initial_amount_cents"] for i in investments)
    total_current = sum(i["current_amount_cents"] for i in investments)
    total_profit = total_current - total_invested
    profit_percentage = (total_profit / total_invested * 100) if total_invested > 0 else 0

    # Agrupar por tipo
    by_type = {}
    for inv in investments:
        t = inv["type"]
        if t not in by_type:
            by_type[t] = {"type": t, "total_cents": 0, "count": 0}
        by_type[t]["total_cents"] += inv["current_amount_cents"]
        by_type[t]["count"] += 1

    # Agrupar por instituição
    by_institution = {}
    for inv in investments:
        inst = inv.get("institution") or "Não informada"
        if inst not in by_institution:
            by_institution[inst] = {"institution": inst, "total_cents": 0, "count": 0}
        by_institution[inst]["total_cents"] += inv["current_amount_cents"]
        by_institution[inst]["count"] += 1

    return InvestmentSummaryResponse(
        total_invested_cents=total_invested,
        total_current_cents=total_current,
        total_profit_cents=total_profit,
        profit_percentage=round(profit_percentage, 2),
        by_type=list(by_type.values()),
        by_institution=list(by_institution.values()),
    )


@router.get("/{investment_id}", response_model=InvestmentResponse)
async def get_investment(investment_id: str):
    """Detalha um investimento específico"""
    response = (
        supabase.table("investments").select("*").eq("id", investment_id).execute()
    )
    if not response.data:
        raise HTTPException(404, "Investimento não encontrado")
    return response.data[0]


@router.post("/", response_model=InvestmentResponse)
async def create_investment(data: InvestmentCreate):
    """Registra um novo investimento."""
    insert_data = data.model_dump()
    insert_data["type"] = data.type.value
    insert_data["purchase_date"] = data.purchase_date.isoformat()
    if data.maturity_date:
        insert_data["maturity_date"] = data.maturity_date.isoformat()
    insert_data["is_active"] = True

    response = supabase.table("investments").insert(insert_data).execute()
    if not response.data:
        raise HTTPException(500, "Erro ao criar investimento")

    # Registrar no histórico
    supabase.table("investment_history").insert(
        {
            "investment_id": response.data[0]["id"],
            "amount_cents": data.current_amount_cents,
            "source": "initial",
        }
    ).execute()

    return response.data[0]


@router.put("/{investment_id}", response_model=InvestmentResponse)
async def update_investment(investment_id: str, data: InvestmentUpdate):
    """Atualiza um investimento."""
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}

    if "type" in update_data:
        update_data["type"] = update_data["type"].value
    if "maturity_date" in update_data:
        update_data["maturity_date"] = update_data["maturity_date"].isoformat()

    response = (
        supabase.table("investments")
        .update(update_data)
        .eq("id", investment_id)
        .execute()
    )
    if not response.data:
        raise HTTPException(404, "Investimento não encontrado")

    return response.data[0]


@router.post("/{investment_id}/update-value")
async def update_investment_value(
    investment_id: str,
    current_amount_cents: int = Query(..., gt=0),
):
    """
    Atualiza apenas o valor atual do investimento.
    Gera um registro no histórico.
    """
    # Atualizar valor
    response = (
        supabase.table("investments")
        .update({"current_amount_cents": current_amount_cents})
        .eq("id", investment_id)
        .execute()
    )
    if not response.data:
        raise HTTPException(404, "Investimento não encontrado")

    # Registrar no histórico
    supabase.table("investment_history").insert(
        {
            "investment_id": investment_id,
            "amount_cents": current_amount_cents,
            "source": "manual",
        }
    ).execute()

    return response.data[0]


@router.post("/{investment_id}/redeem")
async def redeem_investment(
    investment_id: str,
    amount_cents: int = Query(..., gt=0, description="Valor resgatado em centavos"),
    full_redemption: bool = Query(False),
):
    """
    Registra resgate de um investimento.
    - Resgate parcial: reduz valor atual
    - Resgate total: marca como inativo
    """
    # Buscar investimento atual
    inv_response = (
        supabase.table("investments").select("*").eq("id", investment_id).execute()
    )
    if not inv_response.data:
        raise HTTPException(404, "Investimento não encontrado")

    investment = inv_response.data[0]
    current = investment["current_amount_cents"]

    if amount_cents > current:
        raise HTTPException(400, "Valor de resgate maior que o valor atual")

    if full_redemption or amount_cents >= current:
        # Resgate total
        update_data = {"current_amount_cents": 0, "is_active": False}
    else:
        # Resgate parcial
        update_data = {"current_amount_cents": current - amount_cents}

    response = (
        supabase.table("investments")
        .update(update_data)
        .eq("id", investment_id)
        .execute()
    )

    # Registrar no histórico
    supabase.table("investment_history").insert(
        {
            "investment_id": investment_id,
            "amount_cents": update_data["current_amount_cents"],
            "source": "redemption",
        }
    ).execute()

    return {
        "investment": response.data[0],
        "redeemed_amount_cents": amount_cents,
        "is_full_redemption": full_redemption or amount_cents >= current,
    }


@router.get("/{investment_id}/history", response_model=List[InvestmentHistoryResponse])
async def get_investment_history(investment_id: str):
    """Histórico de atualizações de valor do investimento"""
    response = (
        supabase.table("investment_history")
        .select("*")
        .eq("investment_id", investment_id)
        .order("recorded_at", desc=True)
        .execute()
    )
    return response.data


@router.delete("/{investment_id}")
async def delete_investment(investment_id: str):
    """Remove um investimento"""
    # Remover histórico primeiro
    supabase.table("investment_history").delete().eq(
        "investment_id", investment_id
    ).execute()

    # Remover investimento
    supabase.table("investments").delete().eq("id", investment_id).execute()

    return {"deleted": True, "id": investment_id}
