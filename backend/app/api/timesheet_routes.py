from fastapi import APIRouter

from collections import defaultdict
from datetime import datetime

from app.database.database import SessionLocal
from app.models.time_record import TimeRecord

from app.models.employee import Employee
from app.models.justification import Justification
from app.models.scale import Scale
from app.models.scale_day import ScaleDay

router = APIRouter()


# =====================================================
# TIMESHEET
# =====================================================

@router.get("/timesheet/{registration}")
def get_timesheet(registration: str):

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

        # =================================================
        # AGRUPA POR DATA
        # =================================================

        grouped = defaultdict(list)

        for record in records:

            date_key = str(
                record.record_time.date()
            )

            grouped[date_key].append(
                record
            )

        result = []

        # =================================================
        # PROCESSA CADA DIA
        # =================================================

        for date, day_records in grouped.items():

            employee_name = (
                day_records[0].employee_name
            )



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

            day_scale = None

            if schedule:

                weekday = datetime.strptime(
                    date,
                    "%Y-%m-%d"
                ).weekday()

                nomes = [

                    "MONDAY",
                    "TUESDAY",
                    "WEDNESDAY",
                    "THURSDAY",
                    "FRIDAY",
                    "SATURDAY",
                    "SUNDAY"

                ]

                day_scale = db.query(
                    ScaleDay
                ).filter(

                    ScaleDay.scale_id == schedule.id,

                    ScaleDay.day_name == nomes[weekday]

                ).first()

            


            # =================================================
            # ORDENA CORRETAMENTE
            # =================================================

            ordered = sorted(

                day_records,

                key=lambda x: x.record_time
            )

            # =================================================
            # MONTA BATIDAS NA ORDEM REAL
            # =================================================

            batidas = []

            for r in ordered:

                batidas.append({

                    "id":
                        r.id,

                    "time":
                        r.record_time.strftime(
                            "%H:%M:%S"
                        ),

                    "datetime":
                        r.record_time,

                    "inout":
                        r.inout
                })

            # =================================================
            # GARANTE 6 POSIÇÕES
            # =================================================

            while len(batidas) < 6:

                batidas.append(None)



            # ==========================================
            # JUSTIFICATIVAS
            # ==========================================

            justification = None

            if employee:

                current_day = datetime.strptime(
                    date,
                    "%Y-%m-%d"
                ).date()

                justification = db.query(
                    Justification
                ).filter(

                    Justification.employee_id == employee.id,

                    Justification.start_date <= current_day,

                    Justification.end_date >= current_day

                ).first()


            mapping = {

                "Atestado Médico": "ATEST",

                "Atestado": "ATEST",

                "Férias": "FERIA",

                "Abono": "ABONO",

                "Licença": "LICEN",

                "Folga": "FOLGA"

            }

            hour_slots = [

                False,

                False,

                False,

                False,

                False,

                False

            ]

            just_text = ""

            if justification:

                just_text = mapping.get(

                    justification.justification_type,

                    justification.justification_type.upper()[:5]

                )

                # --------------------------------------
                # DIA INTEIRO
                # --------------------------------------

                if justification.mode == "day":

                    for i in range(6):

                        batidas[i] = {

                            "id": None,

                            "time": just_text,

                            "datetime": None,

                            "inout": None

                        }

                # --------------------------------------
                # POR HORA
                # --------------------------------------

                elif justification.mode == "hour" and day_scale:

                    horarios = [

                        day_scale.entry_1,

                        day_scale.exit_1,

                        day_scale.entry_2,

                        day_scale.exit_2,

                        day_scale.entry_3,

                        day_scale.exit_3

                    ]

                    for idx, horario in enumerate(horarios):

                        if not horario:

                            continue

                        hora = datetime.strptime(

                            horario[:5],

                            "%H:%M"

                        ).time()

                        if (

                            justification.start_time

                            <= hora

                            <=

                            justification.end_time

                        ):

                            batidas[idx] = {

                                "id": None,

                                "time": just_text,

                                "datetime": None,

                                "inout": None

                            }



            # =================================================
            # MAPEAMENTO FIXO
            # =================================================

            entrada_1 = batidas[0]
            saida_1 = batidas[1]

            entrada_2 = batidas[2]
            saida_2 = batidas[3]

            entrada_3 = batidas[4]
            saida_3 = batidas[5]

            # =================================================
            # CALCULA HORAS
            # =================================================

            total_seconds = 0

            pares = [

                (entrada_1, saida_1),

                (entrada_2, saida_2),

                (entrada_3, saida_3)
            ]

            for entrada, saida in pares:

                if (

                    entrada
                    and
                    saida
                    and
                    entrada.get("datetime")
                    and
                    saida.get("datetime")

                ):

                    diferenca = (

                        saida["datetime"]
                        -
                        entrada["datetime"]

                    )

                    segundos = int(
                        diferenca.total_seconds()
                    )

                    # =========================================
                    # EVITA NEGATIVO
                    # =========================================

                    if segundos > 0:

                        total_seconds += segundos

            # =================================================
            # FORMATA HORAS
            # =================================================

            horas = total_seconds // 3600

            minutos = (
                total_seconds % 3600
            ) // 60

            worked_hours = (
                f"{horas:02}:{minutos:02}"
            )

            # =================================================
            # RESULTADO FINAL
            # =================================================

            result.append({

                "date":
                    date,

                "employee":
                    employee_name,

                "entrada_1":
                    entrada_1,

                "saida_1":
                    saida_1,

                "entrada_2":
                    entrada_2,

                "saida_2":
                    saida_2,

                "entrada_3":
                    entrada_3,

                "saida_3":
                    saida_3,

                "worked_hours":
                    worked_hours
            })

        # =================================================
        # ORDENA POR DATA
        # =================================================

        result = sorted(

            result,

            key=lambda x: x["date"],

            reverse=True
        )


        import json

        print("================================")
        print(json.dumps(result, default=str, indent=4))
        print("================================")

        return result

       

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