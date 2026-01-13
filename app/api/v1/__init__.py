from fastapi import APIRouter
from app.api.v1 import dashboard, income, expenses, investments, organizze

router = APIRouter()

router.include_router(dashboard.router)
router.include_router(income.router)
router.include_router(expenses.router)
router.include_router(investments.router)
router.include_router(organizze.router)
