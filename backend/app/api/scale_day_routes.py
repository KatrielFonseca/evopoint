from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.models.scale import Scale
from app.models.scale_day import ScaleDay

from app.schemas.scale_day_schema import (
    ScaleDayCreate
)

router = APIRouter()


# =========================================
# DATABASE
# =========================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================================
# LIST DAYS
# =========================================

@router.get("/scale-days/{scale_id}")
def list_scale_days(
    scale_id: int,
    db: Session = Depends(get_db)
):

    return db.query(ScaleDay).filter(
        ScaleDay.scale_id == scale_id
    ).all()


# =========================================
# CREATE DAY
# =========================================

@router.post("/scale-days")
def create_scale_day(
    day: ScaleDayCreate,
    db: Session = Depends(get_db)
):

    scale = db.query(Scale).filter(
        Scale.id == day.scale_id
    ).first()

    if not scale:

        raise HTTPException(
            status_code=404,
            detail="Escala não encontrada."
        )

    new_day = ScaleDay(

        scale_id=day.scale_id,

        day_name=day.day_name,

        entry_1=day.entry_1,
        exit_1=day.exit_1,

        entry_2=day.entry_2,
        exit_2=day.exit_2,

        entry_3=day.entry_3,
        exit_3=day.exit_3
    )

    db.add(new_day)

    db.commit()

    db.refresh(new_day)

    return new_day


# =========================================
# UPDATE DAY
# =========================================

@router.put("/scale-days/{day_id}")
def update_scale_day(
    day_id: int,
    day: ScaleDayCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(ScaleDay).filter(
        ScaleDay.id == day_id
    ).first()

    if not existing:

        raise HTTPException(
            status_code=404,
            detail="Dia não encontrado."
        )

    existing.day_name = day.day_name

    existing.entry_1 = day.entry_1
    existing.exit_1 = day.exit_1

    existing.entry_2 = day.entry_2
    existing.exit_2 = day.exit_2

    existing.entry_3 = day.entry_3
    existing.exit_3 = day.exit_3

    db.commit()

    db.refresh(existing)

    return existing


# =========================================
# DELETE DAY
# =========================================

@router.delete("/scale-days/{day_id}")
def delete_scale_day(
    day_id: int,
    db: Session = Depends(get_db)
):

    day = db.query(ScaleDay).filter(
        ScaleDay.id == day_id
    ).first()

    if not day:

        raise HTTPException(
            status_code=404,
            detail="Dia não encontrado."
        )

    db.delete(day)

    db.commit()

    return {
        "message": "Dia removido com sucesso."
    }