from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from datetime import datetime

from app.database.database import SessionLocal

from app.models.time_record import TimeRecord

from app.schemas.time_schema import (
    TimeRecordCreate
)

router = APIRouter()


# =====================================================
# DATABASE
# =====================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =====================================================
# CREATE RECORD
# =====================================================

@router.post("/time-records")
def create_record(

    record: TimeRecordCreate,

    db: Session = Depends(get_db)
):

    try:

        # =================================================
        # EVITA DUPLICAÇÃO
        # =================================================

        existing = db.query(TimeRecord).filter(

            TimeRecord.employee_registration
            == str(record.employee_registration),

            TimeRecord.record_time
            == record.record_time

        ).first()

        if existing:

            return {

                "success": False,

                "message":
                    "Registro já existe"
            }

        # =================================================
        # CRIA REGISTRO
        # =================================================

        new_record = TimeRecord(

            employee_registration=
                str(record.employee_registration),

            employee_name=
                str(record.employee_name),

            record_time=
                record.record_time,

            verification_mode=
                getattr(
                    record,
                    "verification_mode",
                    "Manual"
                ),

            device_event=
                getattr(
                    record,
                    "device_event",
                    "0"
                ),

            inout=
                int(record.inout)
        )

        db.add(new_record)

        db.commit()

        db.refresh(new_record)

        print("================================")
        print("NOVO REGISTRO")
        print(new_record.employee_name)
        print(new_record.record_time)
        print("================================")

        return {

            "success": True,

            "id":
                new_record.id,

            "employee_registration":
                new_record.employee_registration,

            "employee_name":
                new_record.employee_name,

            "record_time":
                str(new_record.record_time),

            "inout":
                new_record.inout
        }

    except Exception as e:

        db.rollback()

        print("================================")
        print("ERRO CREATE RECORD")
        print(str(e))
        print("================================")

        return {

            "success": False,

            "error": str(e)
        }


# =====================================================
# LIST RECORDS
# =====================================================

@router.get("/time-records")
def list_records(

    db: Session = Depends(get_db)
):

    try:

        records = db.query(TimeRecord).order_by(

            TimeRecord.record_time.desc()

        ).all()

        result = []

        for r in records:

            result.append({

                "id":
                    r.id,

                "employee_registration":
                    r.employee_registration,

                "employee_name":
                    r.employee_name,

                "record_time":
                    str(r.record_time),

                "verification_mode":
                    r.verification_mode,

                "device_event":
                    r.device_event,

                "inout":
                    r.inout
            })

        return result

    except Exception as e:

        print("================================")
        print("ERRO LIST RECORDS")
        print(str(e))
        print("================================")

        return {

            "success": False,

            "error": str(e)
        }


# =====================================================
# DELETE RECORD
# =====================================================

@router.delete("/time-records/{record_id}")
def delete_record(

    record_id: int,

    db: Session = Depends(get_db)
):

    try:

        record = db.query(TimeRecord).filter(

            TimeRecord.id == record_id

        ).first()

        if not record:

            return {

                "success": False,

                "message":
                    "Registro não encontrado"
            }

        db.delete(record)

        db.commit()

        print("================================")
        print("REGISTRO DELETADO")
        print(record_id)
        print("================================")

        return {

            "success": True,

            "message":
                "Registro deletado"
        }

    except Exception as e:

        db.rollback()

        print("================================")
        print("ERRO DELETE RECORD")
        print(str(e))
        print("================================")

        return {

            "success": False,

            "error": str(e)
        }


# =====================================================
# GET RECORD BY ID
# =====================================================

@router.get("/time-records/{record_id}")
def get_record(

    record_id: int,

    db: Session = Depends(get_db)
):

    try:

        record = db.query(TimeRecord).filter(

            TimeRecord.id == record_id

        ).first()

        if not record:

            return {

                "success": False,

                "message":
                    "Registro não encontrado"
            }

        return {

            "id":
                record.id,

            "employee_registration":
                record.employee_registration,

            "employee_name":
                record.employee_name,

            "record_time":
                str(record.record_time),

            "verification_mode":
                record.verification_mode,

            "device_event":
                record.device_event,

            "inout":
                record.inout
        }

    except Exception as e:

        print("================================")
        print("ERRO GET RECORD")
        print(str(e))
        print("================================")

        return {

            "success": False,

            "error": str(e)
        }