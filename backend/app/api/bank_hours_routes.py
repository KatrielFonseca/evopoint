from fastapi import APIRouter

from app.services.bank_hours_service import (
    calculate_bank_hours
)

router = APIRouter()

# =========================================
# BANCO DE HORAS
# =========================================

@router.get("/bank-hours")
def get_bank_hours():

    return calculate_bank_hours()