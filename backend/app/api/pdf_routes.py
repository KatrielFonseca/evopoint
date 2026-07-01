print("####################################")
print("PDF_ROUTES CARREGADO")
print(__file__)
print("####################################")
import traceback
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
from app.models.justification import Justification
from zipfile import ZipFile
import tempfile
import os
from app.models.settings import Settings



from app.calculations.worked_time import justified_seconds



from PySide6.QtWidgets import QFileDialog
from datetime import timedelta


from app.services.timesheet_service import (
    build_timesheet
)

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
        
        settings = db.query(Settings).first()

        cnpj = ""

        if settings:

            cnpj = settings.cnpj or ""


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

        if start_date and end_date:

            start_dt = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            )

            end_dt = (
                datetime.strptime(
                    end_date,
                    "%Y-%m-%d"
                )
                +
                timedelta(days=1)
            )

            query = query.filter(

                TimeRecord.record_time >= start_dt,

                TimeRecord.record_time < end_dt

            )

        records = query.order_by(

            TimeRecord.record_time.asc()

        ).all()

        if records:

            if start_date:

                period_start = datetime.strptime(
                    start_date,
                    "%Y-%m-%d"
                )

            else:

                period_start = min(
                    r.record_time
                    for r in records
                )

            if end_date:

                period_end = datetime.strptime(
                    end_date,
                    "%Y-%m-%d"
                )

            else:

                period_end = max(
                    r.record_time
                    for r in records
                )

        else:

            if not start_date or not end_date:

                return {
                    "success": False,
                    "error": "Período não informado"
                }

            period_start = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            )

            period_end = datetime.strptime(
                end_date,
                "%Y-%m-%d"
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
        # JUSTIFICATIVAS
        # =================================================

        justifications = db.query(
            Justification
        ).filter(
            Justification.employee_id == employee.id
        ).all()

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

                "AVAPoint",

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

        admissao = ""

        if employee.admission_date:

            admissao = employee.admission_date.strftime("%d/%m/%Y")

        info_data = [

            ["Empresa", employee.company, "Horário"],

            ["CNPJ", cnpj, f"SEG {seg}"],

            ["Matrícula", employee.registration, f"TER {ter}"],

            ["Funcionário", employee.name, f"QUA {qua}"],

            ["CPF", employee.cpf, f"QUI {qui}"],

            ["Cargo", employee.role, f"SEX {sex}"],

            ["Departamento", employee.department, f"SAB {sab}"],

            ["Admissão", admissao, f"DOM {dom}"]

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


        dados = build_timesheet(

            db=db,

            employee=employee,

            scale=scale,

            records=records,

            holidays=holidays,

            justifications=justifications,

            start_date=period_start.date(),

            end_date=period_end.date()
        )



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
            "EX50%",
            "EX100%",
            "BSALDO"

        ]]

        total_normais = dados["totals"]["normais"]

        total_faltas = dados["totals"]["faltas"]

        total_extras_50 = dados["totals"]["extras_50"]

        total_extras_100 = dados["totals"]["extras_100"]

        total_carga = dados["totals"]["carga"]

        total_saldo = dados["totals"]["saldo"]
        saldo_acumulado = 0


        

        for day in dados["days"]:

            table_data.append([

                day["day"],

                day["entrada_1"]["time"] if day["entrada_1"] else "",
                day["saida_1"]["time"] if day["saida_1"] else "",

                day["entrada_2"]["time"] if day["entrada_2"] else "",
                day["saida_2"]["time"] if day["saida_2"] else "",

                day["entrada_3"]["time"] if day["entrada_3"] else "",
                day["saida_3"]["time"] if day["saida_3"] else "",

                day["normais"],

                day["faltas"],

                day["extra_50"],

                day["extra_100"],

                day["saldo"]

            ])

        # =================================================
        # TOTAL
        # =================================================


        saldo_final = total_saldo

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

                42,  # NORMAIS
                42,  # FALTAS
                42,  # EX50
                42,  # EX100
                45   # SALDO

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
            seconds_to_hours(total_normais),

            "FALTAS",
            seconds_to_hours(total_faltas),

            "EX50%",
            seconds_to_hours(total_extras_50),

            "EX100%",
            seconds_to_hours(total_extras_100),

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

        print("================================")
        print("ERRO PDF")
        traceback.print_exc()
        print("================================")

        return {

            "success": False,

            "error": str(e)

        }

    finally:

        db.close()


