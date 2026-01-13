from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date
from app.services.organizze_client import organizze_client

router = APIRouter(prefix="/organizze", tags=["Organizze"])


@router.get("/user")
async def get_current_user():
    """Retorna dados do usuário autenticado no Organizze"""
    try:
        return await organizze_client.get_user()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
async def list_categories():
    """Lista todas as categorias do Organizze"""
    try:
        return await organizze_client.get_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/accounts")
async def list_accounts():
    """Lista todas as contas bancárias do Organizze"""
    try:
        return await organizze_client.get_accounts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transactions")
async def list_transactions(
    start_date: date = Query(...),
    end_date: date = Query(...),
    account_id: Optional[int] = Query(None),
):
    """Lista transações do Organizze por período"""
    try:
        return await organizze_client.get_transactions(
            start_date=start_date,
            end_date=end_date,
            account_id=account_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/credit-cards")
async def list_credit_cards():
    """Lista cartões de crédito do Organizze"""
    try:
        return await organizze_client.get_credit_cards()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/budgets/{year}")
async def list_budgets(year: int, month: Optional[int] = Query(None, ge=1, le=12)):
    """Lista metas/budgets do Organizze"""
    try:
        return await organizze_client.get_budgets(year=year, month=month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
