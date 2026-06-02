from fastapi import APIRouter
from fastapi import Query

from datetime import datetime

from app.database.database import SessionLocal
from app.models.time_record import TimeRecord
from app.devices_evo.commands import EvoCommands

router = APIRouter()

# =====================================================
# IGNORA LOGS ANTIGOS AO INICIAR
# =====================================================

SERVICE_STARTED_AT = datetime.now()

print("================================")
print("TIME RECORD ROUTES")
print("================================")
print("IGNORANDO LOGS ANTERIORES A:")
print(SERVICE_STARTED_AT)
print("================================")


# =====================================================
# REGISTROS EM TEMPO REAL
# =====================================================

@router.get("/time-records/realtime")
def get_realtime_records():

    db = SessionLocal()

    try:

        evo = EvoCommands("192.168.88.9")

        logs = evo.get_real_time_logs()

        records = logs.get("record", [])

        for log in records:

            try:

                enrollid = str(
                    log.get("enrollid", "")
                ).strip()

                # =====================================
                # IGNORA REGISTROS INVÁLIDOS
                # =====================================

                if not enrollid:

                    continue

                if enrollid == "99999999":

                    continue

                employee_name = str(
                    log.get("name", "")
                ).strip()

                if not employee_name:

                    employee_name = "Sem Nome"

                # =====================================
                # DATETIME
                # =====================================

                log_time = datetime.strptime(

                    str(log.get("time")),

                    "%Y-%m-%d %H:%M:%S"
                )

                # =====================================
                # IGNORA LOGS ANTIGOS
                # =====================================

                if log_time < SERVICE_STARTED_AT:

                    continue

                # =====================================
                # EVENTO
                # =====================================

                event = str(
                    log.get("event", "0")
                )

                # =====================================
                # USA INOUT REAL DO EQUIPAMENTO
                # =====================================

                inout = int(
                    log.get("inout", 0)
                )

                # =====================================
                # EVITA DUPLICAÇÃO
                # =====================================

                existing = db.query(TimeRecord).filter(

                    TimeRecord.employee_registration
                    == enrollid,

                    TimeRecord.record_time
                    == log_time,

                    TimeRecord.inout
                    == inout

                ).first()

                # =====================================
                # BLOQUEIA DUPLICAÇÃO EM SEGUNDOS
                # =====================================

                last_record = db.query(TimeRecord).filter(

                    TimeRecord.employee_registration
                    == enrollid

                ).order_by(

                    TimeRecord.record_time.desc()

                ).first()

                if last_record:

                    diff = abs(

                        (log_time - last_record.record_time)
                        .total_seconds()

                    )

                    # mesmo tipo muito próximo
                    if diff <= 3 and last_record.inout == inout:

                        continue

                if existing:

                    continue

                # =====================================
                # CRIA REGISTRO
                # =====================================

                novo = TimeRecord(

                    employee_registration=
                        enrollid,

                    employee_name=
                        employee_name,

                    record_time=
                        log_time,

                    verification_mode=
                        "Facial",

                    device_event=
                        event,

                    inout=
                        inout
                )

                db.add(novo)

                print("================================")
                print("NOVO REGISTRO")
                print(employee_name)
                print(log_time)
                print("INOUT:", inout)
                print("================================")

            except Exception as erro_log:

                print("================================")
                print("ERRO PROCESSANDO LOG")
                print(str(erro_log))
                print("================================")

        db.commit()

        # =====================================
        # LISTA REGISTROS
        # =====================================

        registros = db.query(TimeRecord).order_by(

            TimeRecord.record_time.desc()

        ).all()

        resultado = []

        for r in registros:

            resultado.append({

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

        return resultado

    except Exception as e:

        db.rollback()

        print("================================")
        print("ERRO GERAL")
        print(str(e))
        print("================================")

        return {

            "success": False,

            "error": str(e)
        }

    finally:

        db.close()


# =====================================================
# EDITAR REGISTRO
# =====================================================

@router.put("/time-records/{record_id}")
def update_record(

    record_id: int,

    time: str = Query(...),

    inout: int = Query(...)
):

    db = SessionLocal()

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

        # =====================================
        # DATA ORIGINAL
        # =====================================

        original_date = record.record_time.strftime(
            "%Y-%m-%d"
        )

        # =====================================
        # NOVA DATA/HORA
        # =====================================

        new_datetime = datetime.strptime(

            f"{original_date} {time}",

            "%Y-%m-%d %H:%M:%S"
        )

        # =====================================
        # ATUALIZA
        # =====================================

        record.record_time = new_datetime

        record.inout = inout

        db.commit()

        db.refresh(record)

        print("================================")
        print("REGISTRO EDITADO")
        print(record.id)
        print(record.record_time)
        print("================================")

        return {

            "success": True,

            "message":
                "Registro atualizado",

            "id":
                record.id
        }

    except Exception as e:

        db.rollback()

        print("================================")
        print("ERRO UPDATE")
        print(str(e))
        print("================================")

        return {

            "success": False,

            "error": str(e)
        }

    finally:

        db.close()


# =====================================================
# CRIAR REGISTRO MANUAL
# =====================================================

@router.post("/time-records/manual")
def create_manual_record(

    registration: str = Query(...),

    employee_name: str = Query(...),

    date: str = Query(...),

    time: str = Query(...),

    inout: int = Query(...)
):

    db = SessionLocal()

    try:

        full_datetime = datetime.strptime(

            f"{date} {time}",

            "%Y-%m-%d %H:%M:%S"
        )

        # =====================================
        # EVITA DUPLICAÇÃO
        # =====================================

        existing = db.query(TimeRecord).filter(

            TimeRecord.employee_registration
            == registration,

            TimeRecord.record_time
            == full_datetime

        ).first()

        if existing:

            return {

                "success": False,

                "message":
                    "Registro já existe"
            }

        # =====================================
        # CRIA
        # =====================================

        novo = TimeRecord(

            employee_registration=
                registration,

            employee_name=
                employee_name,

            record_time=
                full_datetime,

            verification_mode=
                "Manual",

            device_event=
                "0",

            inout=
                inout
        )

        db.add(novo)

        db.commit()

        db.refresh(novo)

        return {

            "success": True,

            "message":
                "Registro criado",

            "id":
                novo.id
        }

    except Exception as e:

        db.rollback()

        return {

            "success": False,

            "error": str(e)
        }

    finally:

        db.close()

# =====================================================
# EXCLUIR REGISTRO
# =====================================================

@router.delete("/time-records/{record_id}")
def delete_record(record_id: int):

    db = SessionLocal()

    try:

        record = db.query(TimeRecord).filter(
            TimeRecord.id == record_id
        ).first()

        if not record:

            return {
                "success": False,
                "message": "Registro não encontrado"
            }

        db.delete(record)

        db.commit()

        print("================================")
        print("REGISTRO EXCLUÍDO")
        print(record.id)
        print("================================")

        return {
            "success": True,
            "message": "Registro excluído"
        }

    except Exception as e:

        db.rollback()

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        db.close()