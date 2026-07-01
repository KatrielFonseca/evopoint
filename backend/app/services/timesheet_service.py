from collections import defaultdict

from datetime import (
    datetime,
    timedelta
)

from app.models.scale_day import ScaleDay

from app.calculations.worked_time import (
    justified_seconds
)


# =====================================================
# HELPERS
# =====================================================

def seconds_to_hours(seconds):

    seconds = int(seconds)

    horas = seconds // 3600

    minutos = (seconds % 3600) // 60

    return f"{horas:02}:{minutos:02}"


def parse_schedule(scale):

    if not scale:

        return 8 * 3600

    try:

        entrada_1 = datetime.strptime(
            scale.entry_1,
            "%H:%M"
        )

        saida_1 = datetime.strptime(
            scale.exit_1,
            "%H:%M"
        )

        entrada_2 = datetime.strptime(
            scale.entry_2,
            "%H:%M"
        )

        saida_2 = datetime.strptime(
            scale.exit_2,
            "%H:%M"
        )

        return (

            (saida_1 - entrada_1).seconds +

            (saida_2 - entrada_2).seconds

        )

    except:

        return 8 * 3600


def parse_scale_day(day):

    total = 0

    try:

        if day.entry_1 and day.exit_1:

            e1 = datetime.strptime(
                day.entry_1[:5],
                "%H:%M"
            )

            s1 = datetime.strptime(
                day.exit_1[:5],
                "%H:%M"
            )

            total += (
                s1 - e1
            ).seconds

    except:
        pass

    try:

        if day.entry_2 and day.exit_2:

            e2 = datetime.strptime(
                day.entry_2[:5],
                "%H:%M"
            )

            s2 = datetime.strptime(
                day.exit_2[:5],
                "%H:%M"
            )

            total += (
                s2 - e2
            ).seconds

    except:
        pass

    try:

        if day.entry_3 and day.exit_3:

            e3 = datetime.strptime(
                day.entry_3[:5],
                "%H:%M"
            )

            s3 = datetime.strptime(
                day.exit_3[:5],
                "%H:%M"
            )

            total += (
                s3 - e3
            ).seconds

    except:
        pass

    return total


def get_weekday_name(dt):

    dias = [

        "SEG",
        "TER",
        "QUA",
        "QUI",
        "SEX",
        "SAB",
        "DOM"

    ]

    return dias[
        dt.weekday()
    ]


# =====================================================
# BUILD TIMESHEET
# =====================================================

def build_timesheet(

    db,

    employee,

    scale,

    records,

    holidays,

    justifications,

    start_date,

    end_date

):

    grouped = defaultdict(list)

    for record in records:

        grouped[
            str(record.record_time.date())
        ].append(record)

    all_dates = []

    current = start_date

    while current <= end_date:

        all_dates.append(

            current.strftime("%Y-%m-%d")

        )

        current += timedelta(days=1)

    result = []

    total_normais = 0

    total_faltas = 0

    total_extras_50 = 0

    total_extras_100 = 0

    total_carga = 0

    total_saldo = 0

    saldo_acumulado = 0

    # =====================================================
    # PROCESSAMENTO
    # =====================================================

    for date in all_dates:

        day_records = grouped.get(
            date,
            []
        )

        current_date = datetime.strptime(
            date,
            "%Y-%m-%d"
        )

        today = datetime.now().date()

        weekday_map = {

            0: "MONDAY",

            1: "TUESDAY",

            2: "WEDNESDAY",

            3: "THURSDAY",

            4: "FRIDAY",

            5: "SATURDAY",

            6: "SUNDAY"

        }

        weekday_name = weekday_map[
            current_date.weekday()
        ]

        if scale:

            day_scale = db.query(
                ScaleDay
            ).filter(

                ScaleDay.scale_id == scale.id,

                ScaleDay.day_name == weekday_name

            ).first()

        else:

            day_scale = None

        if day_scale:

            carga_diaria = parse_scale_day(
                day_scale
            )

        else:

            carga_diaria = parse_schedule(
                scale
            )

        weekday = current_date.weekday()

        is_saturday = weekday == 5

        is_sunday = weekday == 6

        is_holiday = date in holidays

        ordered = sorted(

            day_records,

            key=lambda x: x.record_time

        )

        batidas = []

        for item in ordered:

            batidas.append({

                "id": item.id,

                "time": item.record_time.strftime("%H:%M"),

                "datetime": item.record_time,

                "inout": item.inout

            })

        while len(batidas) < 6:

            batidas.append(None)


        # =====================================
        # HORAS TRABALHADAS
        # =====================================

        worked_seconds = 0

        justification_day = False

        hour_justification = None

        for j in justifications:

            if str(j.start_date) <= date <= str(j.end_date):

                if j.mode == "day":

                    justification_day = True

                elif j.mode == "hour":

                    hour_justification = j

        pares = [

            (0, 1),

            (2, 3),

            (4, 5)

        ]

        for entrada_i, saida_i in pares:

            entrada = batidas[entrada_i]

            saida = batidas[saida_i]

            if entrada and saida:

                diff = (

                    saida["datetime"]

                    -

                    entrada["datetime"]

                )

                sec = int(

                    diff.total_seconds()

                )

                if sec > 0:

                    worked_seconds += sec

        # =====================================
        # HORAS JUSTIFICADAS
        # =====================================

        worked_seconds += justified_seconds(

            day_scale,

            hour_justification

        )

        faltas = 0

        extras_50 = 0

        extras_100 = 0

        if justification_day:

            worked_seconds = carga_diaria

            faltas = 0

            extras_50 = 0

            extras_100 = 0

        # =====================================
        # FERIADOS
        # =====================================

        if is_holiday:

            extras_100 = worked_seconds

            faltas = 0

        elif is_sunday and (

            not scale

            or

            not scale.sunday

        ):

            extras_100 = worked_seconds

        elif is_saturday and (

            not scale

            or

            not scale.saturday

        ):

            extras_50 = worked_seconds

        else:

            if current_date.date() > today:

                faltas = 0

            elif current_date.date() == today:

                faltas = 0

            elif worked_seconds < carga_diaria:

                faltas = (

                    carga_diaria

                    -

                    worked_seconds

                )

            elif worked_seconds > carga_diaria:

                extras_50 = (

                    worked_seconds

                    -

                    carga_diaria

                )

        if justification_day:

            worked_seconds = carga_diaria

            normais_dia = carga_diaria

            faltas = 0

        hour_slots = [

            False,

            False,

            False,

            False,

            False,

            False

        ]

        if hour_justification:

            inicio = hour_justification.start_time

            fim = hour_justification.end_time

            pares_horarios = [

                day_scale.entry_1 if day_scale else None,

                day_scale.exit_1 if day_scale else None,

                day_scale.entry_2 if day_scale else None,

                day_scale.exit_2 if day_scale else None,

                day_scale.entry_3 if day_scale else None,

                day_scale.exit_3 if day_scale else None

            ]

            for idx, horario in enumerate(pares_horarios):

                if horario:

                    try:

                        hora = datetime.strptime(

                            horario[:5],

                            "%H:%M"

                        ).time()

                        if inicio <= hora <= fim:

                            hour_slots[idx] = True

                    except:

                        pass

        just_text = ""

        if justification_day:

            for j in justifications:

                if str(j.start_date) <= date <= str(j.end_date):

                    mapping = {

                        "Atestado Médico": "ATEST",

                        "Atestado": "ATEST",

                        "Folga": "FOLGA",

                        "Folga Compensada": "FOLGA",

                        "Férias": "FERIA",

                        "Abono": "ABONO",

                        "Licença": "LICEN",

                        "Licença Médica": "LICMD"

                    }

                    just_text = mapping.get(

                        j.justification_type,

                        j.justification_type.upper()[:5]

                    )

                    break

        if justification_day:

            normais_dia = carga_diaria

        elif is_holiday:

            normais_dia = 0

        else:

            normais_dia = min(
                worked_seconds,
                carga_diaria
            )

        if current_date.date() >= today:

            saldo = 0

        elif justification_day:

            saldo = 0

        elif is_holiday:

            saldo = 0

        elif is_sunday and (

            not scale

            or

            not scale.sunday

        ):

            saldo = 0

        elif is_saturday and (

            not scale

            or

            not scale.saturday

        ):

            saldo = 0

        else:

            saldo = (

                worked_seconds

                -

                carga_diaria

            )
        
                # =====================================
        # TOTAIS
        # =====================================

        total_normais += normais_dia

        total_faltas += faltas

        total_extras_50 += extras_50

        total_extras_100 += extras_100

        total_carga += carga_diaria

        total_saldo += saldo

        saldo_acumulado += saldo

        if saldo_acumulado >= 0:

            saldo_text = (

                "+"

                +

                seconds_to_hours(
                    saldo_acumulado
                )

            )

        else:

            saldo_text = (

                "-"

                +

                seconds_to_hours(
                    abs(
                        saldo_acumulado
                    )
                )

            )

        data_formatada = (

            f"{get_weekday_name(current_date)} "

            f"{current_date.strftime('%d/%m/%Y')}"

        )

        result.append({

            "date": date,

            "day":

                data_formatada,

            "entrada_1": (

                None

                if not batidas[0] and not justification_day and not hour_slots[0]

                else {

                    "id": batidas[0]["id"] if batidas[0] else None,

                    "time":

                        just_text

                        if justification_day

                        else (

                            "ATEST"

                            if hour_slots[0]

                            else (

                                batidas[0]["time"]

                                if batidas[0]

                                else ""

                            )

                        )

                }

            ),

            "saida_1": (

                None

                if not batidas[1] and not justification_day and not hour_slots[1]

                else {

                    "id": batidas[1]["id"] if batidas[1] else None,

                    "time":

                        just_text

                        if justification_day

                        else (

                            "ATEST"

                            if hour_slots[1]

                            else (

                                batidas[1]["time"]

                                if batidas[1]

                                else ""

                            )

                        )

                }

            ),

            "entrada_2": (

                None

                if not batidas[2] and not justification_day and not hour_slots[2]

                else {

                    "id": batidas[2]["id"] if batidas[2] else None,

                    "time":

                        just_text

                        if justification_day

                        else (

                            "ATEST"

                            if hour_slots[2]

                            else (

                                batidas[2]["time"]

                                if batidas[2]

                                else ""

                            )

                        )

                }

            ),

            "saida_2": (

                None

                if not batidas[3] and not justification_day and not hour_slots[3]

                else {

                    "id": batidas[3]["id"] if batidas[3] else None,

                    "time":

                        just_text

                        if justification_day

                        else (

                            "ATEST"

                            if hour_slots[3]

                            else (

                                batidas[3]["time"]

                                if batidas[3]

                                else ""

                            )

                        )

                }

            ),

            "entrada_3": (

                None

                if not batidas[4] and not justification_day and not hour_slots[4]

                else {

                    "id": batidas[4]["id"] if batidas[4] else None,

                    "time":

                        just_text

                        if justification_day

                        else (

                            "ATEST"

                            if hour_slots[4]

                            else (

                                batidas[4]["time"]

                                if batidas[4]

                                else ""

                            )

                        )

                }

            ),

            "saida_3": (

                None

                if not batidas[5] and not justification_day and not hour_slots[5]

                else {

                    "id": batidas[5]["id"] if batidas[5] else None,

                    "time":

                        just_text

                        if justification_day

                        else (

                            "ATEST"

                            if hour_slots[5]

                            else (

                                batidas[5]["time"]

                                if batidas[5]

                                else ""

                            )

                        )

                }

            ),

            "normais":

                seconds_to_hours(
                    normais_dia
                ),

            "faltas":

                seconds_to_hours(
                    faltas
                ),

            "extra_50":

                seconds_to_hours(
                    extras_50
                ),

            "extra_100":

                seconds_to_hours(
                    extras_100
                ),

            "saldo":

                saldo_text,

            "worked_seconds":

                worked_seconds,

            "carga_diaria":

                carga_diaria,

            "is_holiday":

                is_holiday,

            "is_saturday":

                is_saturday,

            "is_sunday":

                is_sunday,

            "justification":

                just_text,

            "day_scale":

                day_scale,

            "employee": employee.name,

            "worked_hours": seconds_to_hours(worked_seconds)

        })

    # =====================================
    # RETORNO
    # =====================================

    return {

    "days": result,

    "totals": {

        "normais": total_normais,

        "faltas": total_faltas,

        "extras_50": total_extras_50,

        "extras_100": total_extras_100,

        "saldo": total_saldo,

        "saldo_text":

            ("+" + seconds_to_hours(total_saldo))

            if total_saldo >= 0

            else

            ("-" + seconds_to_hours(abs(total_saldo))),

        "carga": total_carga

    }

}