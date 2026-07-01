from fastapi import APIRouter


from app.database.database import SessionLocal
from app.models.time_record import TimeRecord

from app.models.employee import Employee
from app.models.justification import Justification
from app.models.scale import Scale


from app.services.timesheet_service import (
    build_timesheet
)

from app.models.holiday import Holiday

from datetime import date

router = APIRouter()


# =====================================================
# TIMESHEET
# =====================================================

@router.get("/timesheet/{registration}")
def get_timesheet(
    registration: str,
    start_date: date,
    end_date: date
):

    db = SessionLocal()

    try:

        # =================================================
        # BUSCA REGISTROS
        # =================================================

        records = db.query(TimeRecord).filter(

            TimeRecord.employee_registration
            == registration

        ).order_by(

            TimeRecord.record_time.asc()

        ).all()




        # ==========================================
        # FUNCIONÁRIO
        # ==========================================

        employee = db.query(Employee).filter(
            Employee.registration == registration
        ).first()

        schedule = None

        if employee and employee.schedule:

            schedule = db.query(Scale).filter(
                Scale.name == employee.schedule
            ).first()



        holidays = {

            str(item.date)

            for item in db.query(
                Holiday
            ).all()

        }

        justifications = db.query(
            Justification
        ).filter(

            Justification.employee_id == employee.id

        ).all()




        scale = None

        if employee and employee.schedule:

            scale = db.query(Scale).filter(
                Scale.name == employee.schedule
            ).first()


        


        dados = build_timesheet(

            db=db,

            employee=employee,

            scale=scale,

            records=records,

            holidays=holidays,

            justifications=justifications,

            start_date=start_date,

            end_date=end_date

        )

        return dados["days"]

    except Exception as e:

        print("================================")

        print("ERRO TIMESHEET")

        print(str(e))

        print("================================")

        return {

            "success": False,

            "error": str(e)

        }

    finally:

        db.close()

      