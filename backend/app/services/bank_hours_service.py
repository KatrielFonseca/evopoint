from collections import defaultdict
from datetime import datetime

from app.database.database import SessionLocal

from app.models.employee import Employee
from app.models.time_record import TimeRecord
from app.models.scale import Scale


# =========================================
# HELPERS
# =========================================

def seconds_to_hours(seconds):

    hours = abs(seconds) // 3600

    minutes = (abs(seconds) % 3600) // 60

    return f"{hours:02}:{minutes:02}"


def calculate_scale_workload(scale):

    total = 0

    try:

        e1 = datetime.strptime(
            scale.entry_1,
            "%H:%M"
        )

        s1 = datetime.strptime(
            scale.exit_1,
            "%H:%M"
        )

        total += (
            s1 - e1
        ).seconds

    except:
        pass

    try:

        e2 = datetime.strptime(
            scale.entry_2,
            "%H:%M"
        )

        s2 = datetime.strptime(
            scale.exit_2,
            "%H:%M"
        )

        total += (
            s2 - e2
        ).seconds

    except:
        pass

    try:

        if scale.entry_3 and scale.exit_3:

            e3 = datetime.strptime(
                scale.entry_3,
                "%H:%M"
            )

            s3 = datetime.strptime(
                scale.exit_3,
                "%H:%M"
            )

            total += (
                s3 - e3
            ).seconds

    except:
        pass

    return total


# =========================================
# CALCULAR BANCO
# =========================================

def calculate_bank_hours():

    db = SessionLocal()

    try:

        employees = db.query(
            Employee
        ).all()

        resultado = []

        for employee in employees:

            scale = db.query(
                Scale
            ).filter(

                Scale.name ==
                employee.schedule

            ).first()

            if not scale:

                continue

            carga_diaria = (
                calculate_scale_workload(
                    scale
                )
            )

            records = db.query(
                TimeRecord
            ).filter(

                TimeRecord.employee_registration
                ==
                employee.registration

            ).order_by(

                TimeRecord.record_time.asc()

            ).all()

            grouped = defaultdict(list)

            for record in records:

                data = str(
                    record.record_time.date()
                )

                grouped[data].append(
                    record
                )

            total_normais = 0
            total_extras = 0
            total_faltas = 0

            for _, day_records in grouped.items():

                ordered = sorted(

                    day_records,

                    key=lambda x:
                    x.record_time
                )

                worked_seconds = 0

                pares = [

                    (0, 1),
                    (2, 3),
                    (4, 5)
                ]

                for entrada_i, saida_i in pares:

                    if len(ordered) <= saida_i:

                        continue

                    entrada = ordered[
                        entrada_i
                    ]

                    saida = ordered[
                        saida_i
                    ]

                    diff = (

                        saida.record_time
                        -
                        entrada.record_time

                    )

                    seconds = int(
                        diff.total_seconds()
                    )

                    if seconds > 0:

                        worked_seconds += (
                            seconds
                        )

                if worked_seconds < carga_diaria:

                    total_faltas += (

                        carga_diaria
                        -
                        worked_seconds

                    )

                    total_normais += (
                        worked_seconds
                    )

                else:

                    total_normais += (
                        carga_diaria
                    )

                    total_extras += (

                        worked_seconds
                        -
                        carga_diaria

                    )

            saldo = (
                total_extras
                -
                total_faltas
            )

            if saldo >= 0:

                saldo_text = (

                    "+"
                    +
                    seconds_to_hours(
                        saldo
                    )

                )

            else:

                saldo_text = (

                    "-"
                    +
                    seconds_to_hours(
                        saldo
                    )

                )

            resultado.append({

                "registration":
                    employee.registration,

                "name":
                    employee.name,

                "normal_hours":
                    seconds_to_hours(
                        total_normais
                    ),

                "extra_hours":
                    seconds_to_hours(
                        total_extras
                    ),

                "missing_hours":
                    seconds_to_hours(
                        total_faltas
                    ),

                "balance":
                    saldo_text
            })

        return resultado

    finally:

        db.close()