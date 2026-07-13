from fastapi import APIRouter, HTTPException

from app.database.database import SessionLocal
from app.models.holiday import Holiday
from app.schemas.holiday_schema import HolidayCreate


router = APIRouter(
    prefix="/holidays",
    tags=["Holidays"]
)


# =====================================================
# LISTAR FERIADOS
# =====================================================

@router.get("/")
def get_holidays():

    db = SessionLocal()

    try:

        holidays = (

            db.query(Holiday)

            .order_by(Holiday.date.asc())

            .all()

        )

        return [

            {
                "id": holiday.id,
                "date": holiday.date.isoformat(),
                "description": holiday.description
            }

            for holiday in holidays

        ]

    finally:

        db.close()


# =====================================================
# ADICIONAR FERIADO
# =====================================================

@router.post("/")
def create_holiday(data: HolidayCreate):

    db = SessionLocal()

    try:

        # Evita duplicidade
        exists = (

            db.query(Holiday)

            .filter(
                Holiday.date == data.date
            )

            .first()

        )

        if exists:

            raise HTTPException(

                status_code=400,

                detail="Já existe um feriado cadastrado para esta data."

            )

        holiday = Holiday(

            date=data.date,

            description=data.description.strip()

        )

        db.add(holiday)

        db.commit()

        db.refresh(holiday)

        return {

            "success": True,

            "id": holiday.id,

            "message": "Feriado cadastrado com sucesso."

        }

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# =====================================================
# EXCLUIR FERIADO
# =====================================================

@router.delete("/{holiday_id}")
def delete_holiday(holiday_id: int):

    db = SessionLocal()

    try:

        holiday = (

            db.query(Holiday)

            .filter(
                Holiday.id == holiday_id
            )

            .first()

        )

        if holiday is None:

            raise HTTPException(

                status_code=404,

                detail="Feriado não encontrado."

            )

        db.delete(holiday)

        db.commit()

        return {

            "success": True,

            "message": "Feriado removido com sucesso."

        }

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()