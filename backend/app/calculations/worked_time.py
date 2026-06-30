from datetime import datetime


def _to_seconds(hora_str):

    if not hora_str:
        return None

    return datetime.strptime(
        hora_str[:5],
        "%H:%M"
    ).hour * 3600 + datetime.strptime(
        hora_str[:5],
        "%H:%M"
    ).minute * 60


def _time_to_seconds(t):

    if t is None:
        return None

    return t.hour * 3600 + t.minute * 60 + t.second


def _intersection(start1, end1, start2, end2):

    inicio = max(start1, start2)

    fim = min(end1, end2)

    if fim <= inicio:

        return 0

    return fim - inicio


def justified_seconds(day_scale, justification):

    """
    Calcula quantos segundos da jornada foram
    cobertos pela justificativa.

    Funciona igual ao Secullum.

    Retorna apenas o tempo da escala
    que foi justificado.
    """

    if not day_scale:

        return 0

    if not justification:

        return 0

    if justification.mode != "hour":

        return 0

    inicio = _time_to_seconds(
        justification.start_time
    )

    fim = _time_to_seconds(
        justification.end_time
    )

    total = 0

    periodos = [

        (

            day_scale.entry_1,

            day_scale.exit_1

        ),

        (

            day_scale.entry_2,

            day_scale.exit_2

        ),

        (

            day_scale.entry_3,

            day_scale.exit_3

        )

    ]

    for entrada, saida in periodos:

        if not entrada or not saida:

            continue

        e = _to_seconds(entrada)

        s = _to_seconds(saida)

        total += _intersection(

            e,
            s,

            inicio,
            fim

        )

    return total