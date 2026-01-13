import httpx
from typing import Optional, List
from datetime import date
from app.config import settings


class OrganizzeClient:
    """Cliente para a API do Organizze"""

    BASE_URL = "https://api.organizze.com.br/rest/v2"

    def __init__(self):
        self.auth = (settings.organizze_email, settings.organizze_token)
        self.headers = {
            "User-Agent": f"{settings.app_name} ({settings.contact_email})",
            "Content-Type": "application/json",
        }

    async def _request(self, method: str, endpoint: str, **kwargs) -> dict | list:
        """Faz requisição à API do Organizze"""
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{self.BASE_URL}{endpoint}",
                auth=self.auth,
                headers=self.headers,
                timeout=30.0,
                **kwargs,
            )
            response.raise_for_status()
            return response.json()

    # === TRANSACTIONS ===
    async def get_transactions(
        self,
        start_date: date,
        end_date: date,
        account_id: Optional[int] = None,
    ) -> List[dict]:
        """
        Busca movimentações por período.
        Receitas têm amount_cents > 0, despesas têm amount_cents < 0.
        """
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        if account_id:
            params["account_id"] = account_id
        return await self._request("GET", "/transactions", params=params)

    async def get_transaction(self, transaction_id: int) -> dict:
        """Detalha uma movimentação específica"""
        return await self._request("GET", f"/transactions/{transaction_id}")

    # === ACCOUNTS ===
    async def get_accounts(self) -> List[dict]:
        """Lista todas as contas bancárias"""
        return await self._request("GET", "/accounts")

    async def get_account(self, account_id: int) -> dict:
        """Detalha uma conta bancária"""
        return await self._request("GET", f"/accounts/{account_id}")

    # === CATEGORIES ===
    async def get_categories(self) -> List[dict]:
        """Lista todas as categorias"""
        return await self._request("GET", "/categories")

    # === BUDGETS (Metas do Organizze) ===
    async def get_budgets(self, year: int, month: Optional[int] = None) -> List[dict]:
        """
        Busca metas do Organizze.
        - /budgets -> mês atual
        - /budgets/2024 -> ano inteiro
        - /budgets/2024/01 -> mês específico
        """
        if month:
            endpoint = f"/budgets/{year}/{month:02d}"
        else:
            endpoint = f"/budgets/{year}"
        return await self._request("GET", endpoint)

    # === CREDIT CARDS ===
    async def get_credit_cards(self) -> List[dict]:
        """Lista cartões de crédito"""
        return await self._request("GET", "/credit_cards")

    async def get_credit_card_invoices(
        self,
        card_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[dict]:
        """Lista faturas de um cartão"""
        params = {}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        return await self._request(
            "GET", f"/credit_cards/{card_id}/invoices", params=params
        )

    # === USER ===
    async def get_user(self) -> dict:
        """Retorna dados do usuário autenticado"""
        return await self._request("GET", "/users/me")


# Singleton
organizze_client = OrganizzeClient()
