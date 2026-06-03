print("####################################")
print("PDF_ROUTES CARREGADO")
print(__file__)
print("####################################")


from fastapi import APIRouter, Query
from fastapi.responses import FileResponse

from app.models.scale_day import ScaleDay
from collections import defaultdict
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib import colors
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4

from app.database.database import SessionLocal

from app.models.employee import Employee
from app.models.time_record import TimeRecord
from app.models.scale import Scale
from app.models.holiday import Holiday
from zipfile import ZipFile
import tempfile
import os

from PySide6.QtWidgets import QFileDialog

router = APIRouter()


# =========================================================
# HELPERS
# =========================================================

def seconds_to_hours(seconds):

    seconds = int(seconds)

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60

    return f"{hours:02}:{minutes:02}"


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

            (saida_1 - entrada_1).seconds

            +

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

def format_day_schedule(day):

    if not day:

        return "Folga"

    horarios = []

    if day.entry_1 and day.exit_1:

        horarios.append(
            f"{day.entry_1} {day.exit_1}"
        )

    if day.entry_2 and day.exit_2:

        horarios.append(
            f"{day.entry_2} {day.exit_2}"
        )

    if day.entry_3 and day.exit_3:

        horarios.append(
            f"{day.entry_3} {day.exit_3}"
        )

    return " | ".join(horarios)


# =========================================================
# PDF
# =========================================================

@router.get(
    "/timesheet/pdf/{registration}"
)
def generate_pdf(

    registration: str,

    start_date: str | None = Query(None),

    end_date: str | None = Query(None)

):

    db = SessionLocal()

    try:

        # =================================================
        # FUNCIONÁRIO
        # =================================================

        employee = db.query(
            Employee
        ).filter(

            Employee.registration
            ==
            registration

        ).first()

        if not employee:

            return {

                "success": False,

                "message":
                    "Funcionário não encontrado"

            }

        schedule_name = (
            employee.schedule or ""
        ).strip()

        scale = db.query(
            Scale
        ).filter(
            Scale.name == schedule_name
        ).first()

        # =================================================
        # REGISTROS
        # =================================================

        query = db.query(
            TimeRecord
        ).filter(

            TimeRecord.employee_registration
            ==
            registration

        )

        if start_date:

            query = query.filter(

                TimeRecord.record_time
                >=
                datetime.strptime(
                    start_date,
                    "%Y-%m-%d"
                )

            )

        if end_date:

            query = query.filter(

                TimeRecord.record_time
                <=
                datetime.strptime(
                    end_date,
                    "%Y-%m-%d"
                )

            )

        records = query.order_by(

            TimeRecord.record_time.asc()

        ).all()

        grouped = defaultdict(
            list
        )

        for record in records:

            date_key = str(
                record.record_time.date()
            )

            grouped[
                date_key
            ].append(
                record
            )

        # =================================================
        # FERIADOS
        # =================================================

        holidays = {

            str(item.date)

            for item in db.query(
                Holiday
            ).all()

        }

        # =================================================
        # PDF
        # =================================================

        pdf_path = (
            f"timesheet_{registration}.pdf"
        )

        doc = SimpleDocTemplate(

            pdf_path,

            pagesize=A4,

            rightMargin=16,
            leftMargin=16,

            topMargin=14,
            bottomMargin=14

        )

        styles = (
            getSampleStyleSheet()
        )

        title_style = ParagraphStyle(

            "title",

            parent=styles["Normal"],

            alignment=TA_CENTER,

            fontName="Helvetica-Bold",

            fontSize=17,

            leading=17,

            textColor=colors.HexColor(
                "#00c853"
            )
        )

        subtitle_style = ParagraphStyle(

            "subtitle",

            parent=styles["Normal"],

            alignment=TA_CENTER,

            fontName="Helvetica",

            fontSize=6.5,

            leading=7
        )

        tiny_style = ParagraphStyle(

            "tiny",

            parent=styles["Normal"],

            alignment=TA_CENTER,

            fontName="Helvetica",

            fontSize=5.5,

            leading=6
        )

        elements = []

        # =================================================
        # HEADER
        # =================================================

        elements.append(

            Paragraph(

                "EVOPoint",

                title_style

            )

        )

        elements.append(

            Paragraph(

                "Sistema inteligente de ponto facial",

                subtitle_style

            )

        )

        elements.append(

            Paragraph(

                f"""
                CARTÃO PONTO<br/>
                Emitido em:
                {datetime.now().strftime("%d/%m/%Y %H:%M")}
                """,

                tiny_style

            )

        )

        elements.append(

            Spacer(
                1,
                6
            )

        )

        if scale:

            scale_days = db.query(
                ScaleDay
            ).filter(
                ScaleDay.scale_id == scale.id
            ).all()

            days_map = {

                day.day_name: day

                for day in scale_days

            }

            seg = format_day_schedule(
                days_map.get("MONDAY")
            )

            ter = format_day_schedule(
                days_map.get("TUESDAY")
            )

            qua = format_day_schedule(
                days_map.get("WEDNESDAY")
            )

            qui = format_day_schedule(
                days_map.get("THURSDAY")
            )

            sex = format_day_schedule(
                days_map.get("FRIDAY")
            )

            sab = format_day_schedule(
                days_map.get("SATURDAY")
            )

            dom = format_day_schedule(
                days_map.get("SUNDAY")
            )

        else:

            seg = ter = qua = qui = sex = sab = dom = "-"

        info_data = [

            ["Empresa", employee.company, "Horário"],

            ["CNPJ", "01.919.625/0001-14", f"SEG {seg}"],

            ["Matrícula", employee.registration, f"TER {ter}"],

            ["Funcionário", employee.name, f"QUA {qua}"],

            ["CPF", employee.cpf, f"QUI {qui}"],

            ["Cargo", employee.role, f"SEX {sex}"],

            ["Departamento", employee.department, f"SAB {sab}"],

            ["", "", f"DOM {dom}"]

        ]

        info_table = Table(

            info_data,

            colWidths=[
                70,
                255,
                140
            ]

        )

        info_table.setStyle(TableStyle([

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

            ("FONTSIZE", (0, 0), (-1, -1), 5.8),

            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cfcfcf")),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),

            ("TOPPADDING", (0, 0), (-1, -1), 2),

            ("LEFTPADDING", (0, 0), (-1, -1), 3),

            ("RIGHTPADDING", (0, 0), (-1, -1), 3),

            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#00c853")),

            ("TEXTCOLOR", (0, 0), (0, -1), colors.white)

        ]))

        elements.append(
            info_table
        )

        elements.append(
            Spacer(1, 8)
        )

        # =================================================
        # TABELA PRINCIPAL
        # =================================================

        table_data = [[

            "DIA",

            "ENT. 1",
            "SAÍ. 1",

            "ENT. 2",
            "SAÍ. 2",

            "ENT. 3",
            "SAÍ. 3",

            "NORMAIS",
            "FALTAS",
            "EXTRAS",
            "CARGA",
            "EX0%",
            "EX50%",
            "EX100%",
            "BSALDO"

        ]]

        total_normais = 0
        total_faltas = 0

        total_extras_0 = 0
        total_extras_50 = 0
        total_extras_100 = 0

        total_carga = 0


        # =================================================
        # PROCESSAMENTO
        # =================================================

        for date, day_records in grouped.items():

            current_date = datetime.strptime(
                date,
                "%Y-%m-%d"
            )

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

            day_scale = db.query(
                ScaleDay
            ).filter(
                ScaleDay.scale_id == scale.id,
                ScaleDay.day_name == weekday_name
            ).first()

            if day_scale:

                carga_diaria = (
                    parse_scale_day(
                        day_scale
                    )
                )

            else:

                carga_diaria = (
                    parse_schedule(
                        scale
                    )
    )


            weekday = current_date.weekday()

            is_saturday = (
                weekday == 5
            )

            is_sunday = (
                weekday == 6
            )

            is_holiday = (
                date in holidays
            )

            ordered = sorted(

                day_records,

                key=lambda x:
                    x.record_time

            )

            batidas = []

            for item in ordered:

                batidas.append({

                    "time":

                        item.record_time.strftime(
                            "%H:%M"
                        ),

                    "datetime":
                        item.record_time

                })

            while len(batidas) < 6:

                batidas.append(
                    None
                )

            worked_seconds = 0

            pares = [

                (0, 1),

                (2, 3),

                (4, 5)

            ]

            for entrada_i, saida_i in pares:

                entrada = batidas[
                    entrada_i
                ]

                saida = batidas[
                    saida_i
                ]

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

            faltas = 0

            extras_0 = 0
            extras_50 = 0
            extras_100 = 0

            # ==========================================
            # FERIADO = 100%
            # ==========================================

            if is_holiday:

                extras_100 = worked_seconds

            # ==========================================
            # DOMINGO FOLGA = 100%
            # ==========================================

            elif is_sunday and (

                not scale

                or

                not scale.sunday

            ):

                extras_100 = worked_seconds

            # ==========================================
            # SÁBADO FOLGA = 100%
            # ==========================================

            elif is_saturday and (

                not scale

                or

                not scale.saturday

            ):

                extras_50 = worked_seconds

            else:

                if worked_seconds < carga_diaria:

                    faltas = (

                        carga_diaria

                        -

                        worked_seconds

                    )

                elif worked_seconds > carga_diaria:

                    extras_0 = (

                        worked_seconds

                        -

                        carga_diaria

                    )

            saldo = (

                worked_seconds

                -

                carga_diaria

            )

            total_normais += worked_seconds
            total_faltas += faltas
            total_extras_0 += extras_0
            total_extras_50 += extras_50
            total_extras_100 += extras_100
            total_carga += carga_diaria

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
                        abs(saldo)
                    )

                )

            data_formatada = (

                f"{get_weekday_name(current_date)} "

                f"{current_date.strftime('%d/%m/%Y')}"

            )

            table_data.append([

                data_formatada,

                batidas[0]["time"] if batidas[0] else "",
                batidas[1]["time"] if batidas[1] else "",

                batidas[2]["time"] if batidas[2] else "",
                batidas[3]["time"] if batidas[3] else "",

                batidas[4]["time"] if batidas[4] else "",
                batidas[5]["time"] if batidas[5] else "",

                seconds_to_hours(
                    min(
                        worked_seconds,
                        carga_diaria
                    )
                ),

                seconds_to_hours(
                    faltas
                ),

                seconds_to_hours(
                    extras_0
                    +
                    extras_50
                    +
                    extras_100
                ),

                seconds_to_hours(
                    carga_diaria
                ),

                seconds_to_hours(
                    extras_0
                ),

                seconds_to_hours(
                    extras_50
                ),

                seconds_to_hours(
                    extras_100
                ),

                saldo_text
            ])

        # =================================================
        # TOTAL
        # =================================================

        saldo_final = (

            total_normais

            -

            total_carga

        )

        if saldo_final >= 0:

            saldo_final_text = (

                "+"

                +

                seconds_to_hours(
                    saldo_final
                )

            )

        else:

            saldo_final_text = (

                "-"

                +

                seconds_to_hours(
                    abs(saldo_final)
                )

            )

        table_data.append([

            "TOTAIS",

            "", "", "", "", "", "",

            seconds_to_hours(
                total_normais
            ),

            seconds_to_hours(
                total_faltas
            ),

            seconds_to_hours(

                total_extras_0

                +

                total_extras_50

                +

                total_extras_100

            ),

            seconds_to_hours(
                total_carga
            ),

            seconds_to_hours(
                total_extras_0
            ),

            seconds_to_hours(
                total_extras_50
            ),

            seconds_to_hours(
                total_extras_100
            ),

            saldo_final_text

        ])
        # =================================================
        # TABELA
        # =================================================

        table = Table(

            table_data,

           colWidths=[

                58,

                34,34,

                34,34,

                34,34,

                40,  # NORMAIS
                40,  # FALTAS
                40,  # EXTRAS
                40,  # CARGA
                40,  # EX0
                40,  # EX50
                40,  # EX100
                42   # BSALDO

            ]
        )

        row_styles = []

        for row_index in range(

            1,

            len(table_data) - 1

        ):

            try:

                data_text = table_data[
                    row_index
                ][0]

                data_text = data_text.split(
                    " "
                )[1]

                dt = datetime.strptime(

                    data_text,

                    "%d/%m/%Y"

                )

                is_weekend = (
                    dt.weekday() >= 5
                )

                is_holiday = (

                    str(
                        dt.date()
                    )

                    in

                    holidays

                )

                if is_weekend or is_holiday:

                    row_styles.append(

                        (

                            "BACKGROUND",

                            (0, row_index),

                            (-1, row_index),

                            colors.HexColor(
                                "#FFF9C4"
                            )

                        )

                    )

                    row_styles.append(

                        (

                            "FONTNAME",

                            (0, row_index),

                            (-1, row_index),

                            "Helvetica-Bold"

                        )

                    )

            except:

                pass

        style_list = [

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#00c853")
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (0, -1),
                (-1, -1),
                "Helvetica-Bold"
            ),

            (
                "BACKGROUND",
                (0, -1),
                (-1, -1),
                colors.HexColor("#f3f3f3")
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                5.4
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.35,
                colors.HexColor("#d2d2d2")
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                2
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                2
            )

        ]

        style_list.extend(
            row_styles
        )

        table.setStyle(
            TableStyle(
                style_list
            )
        )

        elements.append(
            table
        )

        elements.append(
            Spacer(
                1,
                8
            )
        )

        # =================================================
        # RESUMO
        # =================================================

        resumo = Table([[
            "NORMAIS",
            seconds_to_hours(
                total_normais
            ),

            "FALTAS",
            seconds_to_hours(
                total_faltas
            ),

            "EXTRAS",
            seconds_to_hours(

                total_extras_0

                +

                total_extras_50

                +

                total_extras_100

            ),

            "SALDO",
            saldo_final_text
        ]])

        resumo.setStyle(TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor(
                    "#00c853"
                )
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, -1),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica-Bold"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                5.8
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.35,
                colors.HexColor(
                    "#00a844"
                )
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                3
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                3
            )

        ]))

        elements.append(
            resumo
        )

        elements.append(
            Spacer(
                1,
                16
            )
        )

        # =================================================
        # ASSINATURAS
        # =================================================

        assinatura = Table([

            [

                "__________________________________",

                "__________________________________"

            ],

            [

                employee.name,

                "Empresa"

            ]

        ])

        assinatura.setStyle(TableStyle([

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                5.5
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5
            )

        ]))

        elements.append(
            assinatura
        )

        # =================================================
        # BUILD
        # =================================================

        doc.build(
            elements
        )

        return FileResponse(

            path=pdf_path,

            filename=pdf_path,

            media_type="application/pdf"

        )

    except Exception as e:

        print(
            "================================"
        )

        print(
            "ERRO PDF"
        )

        print(
            str(e)
        )

        print(
            "================================"
        )

        return {

            "success": False,

            "error": str(e)

        }

    finally:

        db.close()


