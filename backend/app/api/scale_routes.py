from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.models.scale import Scale

from app.schemas.scale_schema import ScaleCreate

from app.models.scale_day import ScaleDay

from app.utils.system_version import (
    bump_system_version
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
# LIST SCALES
# =========================================

@router.get("/scales")
def list_scales(
    db: Session = Depends(get_db)
):

    return db.query(Scale).order_by(
        Scale.name
    ).all()


# =========================================
# CREATE SCALE
# =========================================

@router.post("/scales")
def create_scale(
    scale: ScaleCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Scale).filter(
        Scale.name == scale.name
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Escala já cadastrada."
        )

    new_scale = Scale(

        name=scale.name,

        monday=scale.monday,
        tuesday=scale.tuesday,
        wednesday=scale.wednesday,
        thursday=scale.thursday,
        friday=scale.friday,

        saturday=scale.saturday,
        sunday=scale.sunday,

        entry_1=scale.entry_1,
        exit_1=scale.exit_1,

        entry_2=scale.entry_2,
        exit_2=scale.exit_2,

        entry_3=scale.entry_3,
        exit_3=scale.exit_3
    )

    db.add(new_scale)

    bump_system_version(db)

    db.commit()

    db.refresh(new_scale)

    return new_scale


# =========================================
# UPDATE SCALE
# =========================================

@router.put("/scales/{scale_id}")
def update_scale(
    scale_id: int,
    scale: ScaleCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Scale).filter(
        Scale.id == scale_id
    ).first()

    if not existing:

        raise HTTPException(
            status_code=404,
            detail="Escala não encontrada."
        )

    existing.name = scale.name

    existing.monday = scale.monday
    existing.tuesday = scale.tuesday
    existing.wednesday = scale.wednesday
    existing.thursday = scale.thursday
    existing.friday = scale.friday

    existing.saturday = scale.saturday
    existing.sunday = scale.sunday

    existing.entry_1 = scale.entry_1
    existing.exit_1 = scale.exit_1

    existing.entry_2 = scale.entry_2
    existing.exit_2 = scale.exit_2

    existing.entry_3 = scale.entry_3
    existing.exit_3 = scale.exit_3

    bump_system_version(db)

    db.commit()

    db.refresh(existing)

    return existing


# =========================================
# DELETE SCALE
# =========================================

@router.delete("/scales/{scale_id}")
def delete_scale(
    scale_id: int,
    db: Session = Depends(get_db)
):

    scale = db.query(Scale).filter(
        Scale.id == scale_id
    ).first()

    if not scale:

        raise HTTPException(
            status_code=404,
            detail="Escala não encontrada."
        )

    db.query(
        ScaleDay
    ).filter(
        ScaleDay.scale_id == scale_id
    ).delete()

    db.delete(scale)

    bump_system_version(db)

    db.commit()

    return {
        "message": "Escala removida com sucesso."
    }