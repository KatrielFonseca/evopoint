from collections import defaultdict
from datetime import date, datetime, time

from fastapi import APIRouter
from sqlalchemy import text

from app.database.database import SessionLocal
from app.models.employee import Employee
from app.models.justification import Justification
from app.models.time_record import TimeRecord
from app.services.realtime_service import REALTIME_STATUS


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# =====================================================
# DASHBOARD
# =====================================================

@router.get("/")
def dashboard():

    db = SessionLocal()

    try:

        hoje = date.today()

        inicio = datetime.combine(
            hoje,
            time.min
        )

        fim = datetime.combine(
            hoje,
            time.max
        )

        # ==========================================
        # TOTAL DE FUNCIONÁRIOS
        # ==========================================

        employees = db.query(Employee).count()

        # ==========================================
        # REGISTROS DE HOJE
        # ==========================================

        records_today = (

            db.query(TimeRecord)

            .filter(

                TimeRecord.record_time >= inicio,
                TimeRecord.record_time <= fim

            )

            .order_by(
                TimeRecord.record_time.asc()
            )

            .all()

        )

        # ==========================================
        # PRESENTES
        # ==========================================

        presentes = len({

            r.employee_registration

            for r in records_today

            if r.employee_registration != "99999999"

        })

        # ==========================================
        # ATIVOS
        # ==========================================

        registros = defaultdict(list)

        for record in records_today:

            if record.employee_registration == "99999999":
                continue

            registros[
                record.employee_registration
            ].append(record)

        ativos = 0

        for lista in registros.values():

            lista.sort(
                key=lambda x: x.record_time
            )

            dentro = False

            for _ in lista:

                dentro = not dentro

            if dentro:

                ativos += 1

        # ==========================================
        # AUSENTES
        # ==========================================

        ausentes = max(

            0,

            employees - presentes

        )

        # ==========================================
        # JUSTIFICATIVAS
        # ==========================================

        justificativas = (

            db.query(Justification)

            .filter(

                Justification.start_date <= hoje,

                Justification.end_date >= hoje

            )

            .count()

        )

        return {

            "employees": employees,

            "presentes": presentes,

            "ausentes": ausentes,

            "justificativas": justificativas,

            "ativos": ativos

        }

    finally:

        db.close()


# =====================================================
# STATUS
# =====================================================

@router.get("/status")
def status():

    db = SessionLocal()

    try:

        try:

            db.execute(
                text("SELECT 1")
            )

            database = True

        except:

            database = False

        return {

            "api": True,

            "database": database,

            "evo": REALTIME_STATUS["evo_online"],

            "capture": REALTIME_STATUS["capture"],

            "time": datetime.now().strftime("%H:%M:%S")

        }

    finally:

        db.close()


@router.get("/chart")
def dashboard_chart():

    db = SessionLocal()

    try:

        hoje = date.today()

        inicio = datetime.combine(
            hoje,
            time.min
        )

        fim = datetime.combine(
            hoje,
            time.max
        )

        registros = (

            db.query(TimeRecord)

            .filter(

                TimeRecord.record_time >= inicio,

                TimeRecord.record_time <= fim

            )

            .all()

        )

        horas = {

            h:0

            for h in range(24)

        }

        for registro in registros:

            horas[
                registro.record_time.hour
            ] += 1

        return [

            {

                "hour": h,

                "count": horas[h]

            }

            for h in range(24)

        ]

    finally:

        db.close()