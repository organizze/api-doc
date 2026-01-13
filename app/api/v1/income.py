from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from typing import List, Optional
from datetime import date
import tempfile
import os

from app.database import supabase
from app.schemas.income import (
    ExpectedIncomeCreate,
    ExpectedIncomeUpdate,
    ExpectedIncomeResponse,
    ActualIncomeResponse,
    IncomeComparisonResponse,
    IncomeStatus,
)
from app.services.organizze_client import organizze_client
from app.services.pdf_parser import PDFParserService

router = APIRouter(prefix="/income", tags=["Recebimentos"])


# === RECEBIMENTOS PREVISTOS (do PDF/manual) ===


@router.post("/expected/upload", response_model=List[ExpectedIncomeResponse])
async def upload_expected_income_pdf(
    file: UploadFile = File(...),
    reference_month: int = Query(..., ge=1, le=12),
    reference_year: int = Query(..., ge=2020),
):
    """
    Upload de PDF com valores previstos de recebimento.
    O sistema extrai automaticamente clientes, valores e datas.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Apenas arquivos PDF são aceitos")

    # Salvar arquivo temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Parsear PDF
        parser = PDFParserService(tmp_path)
        parser.extract_content()
        parsed_items = parser.parse_income_values()

        # Salvar no Supabase
        results = []
        for item in parsed_items:
            data = {
                "source_document": file.filename,
                "client_name": item.client_name,
                "description": item.description,
                "expected_amount_cents": item.amount_cents,
                "expected_date": item.expected_date.isoformat(),
                "status": IncomeStatus.PENDING.value,
                "reference_month": reference_month,
                "reference_year": reference_year,
                "actual_amount_cents": 0,
            }
            response = supabase.table("expected_incomes").insert(data).execute()
            if response.data:
                results.append(response.data[0])

        return results
    finally:
        os.unlink(tmp_path)


@router.get("/expected", response_model=List[ExpectedIncomeResponse])
async def list_expected_income(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020),
    status: Optional[IncomeStatus] = Query(None),
):
    """Lista recebimentos previstos por período"""
    query = (
        supabase.table("expected_incomes")
        .select("*")
        .eq("reference_month", month)
        .eq("reference_year", year)
    )

    if status:
        query = query.eq("status", status.value)

    response = query.order("expected_date").execute()
    return response.data


@router.post("/expected", response_model=ExpectedIncomeResponse)
async def create_expected_income(data: ExpectedIncomeCreate):
    """Cria um recebimento previsto manualmente"""
    insert_data = {
        **data.model_dump(),
        "expected_date": data.expected_date.isoformat(),
        "status": IncomeStatus.PENDING.value,
        "actual_amount_cents": 0,
    }
    response = supabase.table("expected_incomes").insert(insert_data).execute()
    if not response.data:
        raise HTTPException(500, "Erro ao criar recebimento previsto")
    return response.data[0]


@router.put("/expected/{income_id}", response_model=ExpectedIncomeResponse)
async def update_expected_income(income_id: str, data: ExpectedIncomeUpdate):
    """Atualiza um recebimento previsto"""
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if "expected_date" in update_data:
        update_data["expected_date"] = update_data["expected_date"].isoformat()
    if "actual_date" in update_data and update_data["actual_date"]:
        update_data["actual_date"] = update_data["actual_date"].isoformat()
    if "status" in update_data:
        update_data["status"] = update_data["status"].value

    response = (
        supabase.table("expected_incomes")
        .update(update_data)
        .eq("id", income_id)
        .execute()
    )
    if not response.data:
        raise HTTPException(404, "Recebimento não encontrado")
    return response.data[0]


@router.delete("/expected/{income_id}")
async def delete_expected_income(income_id: str):
    """Remove um recebimento previsto"""
    response = (
        supabase.table("expected_incomes").delete().eq("id", income_id).execute()
    )
    return {"deleted": True, "id": income_id}


# === RECEBIMENTOS REAIS (do Organizze) ===


@router.get("/actual", response_model=List[ActualIncomeResponse])
async def get_actual_income(
    start_date: date = Query(...),
    end_date: date = Query(...),
    account_id: Optional[int] = Query(None),
):
    """
    Busca recebimentos reais da API do Organizze.
    Filtra transações com amount_cents > 0 (receitas).
    """
    transactions = await organizze_client.get_transactions(
        start_date=start_date,
        end_date=end_date,
        account_id=account_id,
    )

    # Filtrar apenas receitas (amount_cents > 0)
    incomes = [t for t in transactions if t.get("amount_cents", 0) > 0]

    return [
        ActualIncomeResponse(
            id=t["id"],
            description=t.get("description", ""),
            date=t["date"],
            amount_cents=t["amount_cents"],
            category_id=t.get("category_id"),
            account_id=t["account_id"],
            paid=t.get("paid", False),
        )
        for t in incomes
    ]


# === COMPARAÇÃO ===


@router.get("/comparison", response_model=IncomeComparisonResponse)
async def compare_income(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2020),
):
    """
    Compara recebimentos previstos vs realizados.
    """
    # Buscar previstos do Supabase
    expected_response = (
        supabase.table("expected_incomes")
        .select("*")
        .eq("reference_month", month)
        .eq("reference_year", year)
        .execute()
    )
    expected_items = expected_response.data

    # Buscar reais do Organizze
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    transactions = await organizze_client.get_transactions(
        start_date=start_date,
        end_date=end_date,
    )
    actual_incomes = [t for t in transactions if t.get("amount_cents", 0) > 0]

    # Separar por status
    reconciled = [e for e in expected_items if e["status"] == "received"]
    pending = [e for e in expected_items if e["status"] in ["pending", "overdue"]]

    # Encontrar receitas extras (não previstas)
    reconciled_ids = {e.get("organizze_transaction_id") for e in reconciled}
    extras = [t for t in actual_incomes if t["id"] not in reconciled_ids]

    total_expected = sum(e["expected_amount_cents"] for e in expected_items)
    total_actual = sum(t["amount_cents"] for t in actual_incomes)

    return IncomeComparisonResponse(
        month=month,
        year=year,
        total_expected_cents=total_expected,
        total_actual_cents=total_actual,
        difference_cents=total_actual - total_expected,
        reconciled=reconciled,
        pending=pending,
        extras=[
            ActualIncomeResponse(
                id=t["id"],
                description=t.get("description", ""),
                date=t["date"],
                amount_cents=t["amount_cents"],
                category_id=t.get("category_id"),
                account_id=t["account_id"],
                paid=t.get("paid", False),
            )
            for t in extras
        ],
    )


@router.post("/reconcile/{expected_id}/{transaction_id}")
async def reconcile_income(expected_id: str, transaction_id: int):
    """Reconcilia um recebimento previsto com uma transação real do Organizze."""
    # Buscar transação do Organizze
    transaction = await organizze_client.get_transaction(transaction_id)

    # Atualizar registro no Supabase
    update_data = {
        "status": IncomeStatus.RECEIVED.value,
        "actual_amount_cents": transaction["amount_cents"],
        "actual_date": transaction["date"],
        "organizze_transaction_id": transaction_id,
    }

    response = (
        supabase.table("expected_incomes")
        .update(update_data)
        .eq("id", expected_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(404, "Recebimento previsto não encontrado")

    return response.data[0]
