from fastapi import APIRouter

from app.database.database import SessionLocal

from app.models.justification import (
    Justification
)

from app.schemas.justification_schema import (
    JustificationCreate
)

from app.utils.system_version import (
    bump_system_version
)

from fastapi import Query


from app.models.employee import Employee

router = APIRouter(
    prefix="/justifications",
    tags=["Justifications"]
)

# =========================================
# LISTAR
# =========================================

@router.get("/")
def get_justifications():

    db = SessionLocal()

    try:

        records = (

            db.query(
                Justification,
                Employee.name
            )

            .join(
                Employee,
                Employee.id == Justification.employee_id
            )

            .all()

        )

        return [

            {

                "id": item.id,

                "employee_id": item.employee_id,

                "employee_name": employee_name,

                "start_date": str(item.start_date),

                "end_date": str(item.end_date),

                "mode": item.mode,

                "start_time": str(item.start_time)
                if item.start_time else "",

                "end_time": str(item.end_time)
                if item.end_time else "",

                "justification_type": item.justification_type,

                "description": item.description,

                "attachment": item.attachment

            }

            for item, employee_name in records

        ]

    finally:

        db.close()


# =========================================
# CADASTRAR
# =========================================

@router.post("/")
def create_justification(
    data: JustificationCreate
):

    db = SessionLocal()

    try:

        item = Justification(

            employee_id=
            data.employee_id,

            start_date=
            data.start_date,

            end_date=
            data.end_date,

            mode=data.mode,

            start_time=data.start_time,

            end_time=data.end_time,

            justification_type=
            data.justification_type,

            description=
            data.description,

            attachment=
            data.attachment

        )

        db.add(item)

        bump_system_version(db)

        db.commit()

        return {

            "success": True

        }

    finally:

        db.close()


# =========================================
# EXCLUIR
# =========================================

@router.delete("/{item_id}")
def delete_justification(
    item_id: int
):

    db = SessionLocal()

    try:

        item = db.query(
            Justification
        ).filter(

            Justification.id == item_id

        ).first()

        if not item:

            return {

                "success": False

            }

        db.delete(item)

        bump_system_version(db)

        db.commit()

        return {

            "success": True

        }

    finally:

        db.close()


from datetime import date
from calendar import monthrange


# =========================================
# JUSTIFICATIVAS DO MÊS
# =========================================

@router.get("/month/{year}/{month}")
def get_month_justifications(
    year: int,
    month: int,
    employee_id: int | None = Query(None)
):

    db = SessionLocal()

    try:

        first_day = date(
            year,
            month,
            1
        )

        last_day = date(
            year,
            month,
            monthrange(year, month)[1]
        )

        query = (

            db.query(
                Justification,
                Employee.name
            )

            .join(
                Employee,
                Employee.id == Justification.employee_id
            )

            .filter(

                Justification.start_date <= last_day,

                Justification.end_date >= first_day

            )

        )

        # =====================================
        # FILTRO POR FUNCIONÁRIO
        # =====================================

        if employee_id is not None:

            query = query.filter(

                Justification.employee_id == employee_id

            )

        records = query.all()

        result = []

        for item, employee_name in records:

            result.append({

                "id": item.id,

                "employee_name": employee_name,

                "employee_id": item.employee_id,

                "type": item.justification_type,

                "mode": item.mode,

                "start_date": str(item.start_date),

                "end_date": str(item.end_date),

                "start_time":
                    str(item.start_time)
                    if item.start_time else "",

                "end_time":
                    str(item.end_time)
                    if item.end_time else "",

                "description":
                    item.description

            })

        return result

    finally:

        db.close()