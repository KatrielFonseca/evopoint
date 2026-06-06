from fastapi import APIRouter

from app.database.database import SessionLocal

from app.models.holiday import Holiday

from app.schemas.holiday_schema import (
    HolidayCreate
)

router = APIRouter(
    prefix="/holidays",
    tags=["Holidays"]
)

# =====================================
# LISTAR
# =====================================

@router.get("/")
def get_holidays():

    db = SessionLocal()

    try:

        holidays = db.query(
            Holiday
        ).order_by(
            Holiday.date.asc()
        ).all()

        return [

            {

                "id": item.id,

                "date":
                    str(item.date),

                "description":
                    item.description

            }

            for item in holidays

        ]

    finally:

        db.close()


# =====================================
# ADICIONAR
# =====================================

@router.post("/")
def create_holiday(
    data: HolidayCreate
):

    db = SessionLocal()

    try:

        holiday = Holiday(

            date=data.date,

            description=data.description

        )

        db.add(
            holiday
        )

        bump_system_version(db)

        db.commit()

        return {

            "success": True

        }

    finally:

        db.close()


# =====================================
# EXCLUIR
# =====================================

@router.delete("/{holiday_id}")
def delete_holiday(
    holiday_id: int
):

    db = SessionLocal()

    try:

        holiday = db.query(
            Holiday
        ).filter(

            Holiday.id == holiday_id

        ).first()

        if not holiday:

            return {

                "success": False

            }

        db.delete(
            holiday
        )

        bump_system_version(db)

        db.commit()

        return {

            "success": True

        }

    finally:

        db.close()