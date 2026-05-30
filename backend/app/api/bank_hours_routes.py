from fastapi import APIRouter

from app.database.database import SessionLocal

from app.models.time_record import TimeRecord

from app.services.bank_hours_service import (
    calculate_bank_hours
)

router = APIRouter()

# =========================================
# CONSULTAR
# =========================================

@router.get("/bank-hours")
def get_bank_hours():

    return calculate_bank_hours()


# =========================================
# RECALCULAR
# =========================================

@router.post("/bank-hours/recalculate")
def recalculate_bank_hours():

    return {

        "success": True,

        "message":
            "Banco recalculado com sucesso."

    }


# =========================================
# ZERAR
# =========================================

@router.post("/bank-hours/reset")
def reset_bank_hours():

    db = SessionLocal()

    try:

        db.query(
            TimeRecord
        ).delete()

        db.commit()

        return {

            "success": True,

            "message":
                "Banco zerado com sucesso."

        }

    finally:

        db.close()