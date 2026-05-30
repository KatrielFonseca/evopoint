from fastapi import APIRouter
from fastapi.responses import FileResponse

from collections import defaultdict
from datetime import datetime
from app.models.scale import Scale

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4

from app.database.database import SessionLocal

from app.models.employee import Employee
from app.models.time_record import TimeRecord

router = APIRouter()


# =========================================================
# HELPERS
# =========================================================

def seconds_to_hours(seconds):

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60

    return f"{hours:02}:{minutes:02}"


def parse_schedule(schedule):

    try:

        horarios = schedule.split()

        if len(horarios) >= 4:

            entrada_1 = datetime.strptime(
                horarios[0],
                "%H:%M"
            )

            saida_1 = datetime.strptime(
                horarios[1],
                "%H:%M"
            )

            entrada_2 = datetime.strptime(
                horarios[2],
                "%H:%M"
            )

            saida_2 = datetime.strptime(
                horarios[3],
                "%H:%M"
            )

            carga = (
                (saida_1 - entrada_1).seconds
                +
                (saida_2 - entrada_2).seconds
            )

            return carga

    except:

        pass

    return 8 * 3600


# =========================================================
# PDF
# =========================================================

@router.get("/timesheet/pdf/{registration}")
def generate_pdf(registration: str):

    db = SessionLocal()

    try:

        # =================================================
        # FUNCIONÁRIO
        # =================================================

        employee = db.query(Employee).filter(
            Employee.registration == registration
        ).first()

        if not employee:

            return {
                "success": False,
                "message": "Funcionário não encontrado"
            }

        scale = db.query(Scale).filter(
            Scale.name == employee.schedule
        ).first()

        # =================================================
        # REGISTROS
        # =================================================

        records = db.query(TimeRecord).filter(
            TimeRecord.employee_registration == registration
        ).order_by(
            TimeRecord.record_time.asc()
        ).all()

        grouped = defaultdict(list)

        for record in records:

            key = str(
                record.record_time.date()
            )

            grouped[key].append(record)

        # =================================================
        # PDF CONFIG
        # =================================================

        pdf_path = f"timesheet_{registration}.pdf"

        doc = SimpleDocTemplate(

            pdf_path,

            pagesize=A4,

            rightMargin=16,
            leftMargin=16,

            topMargin=14,
            bottomMargin=14
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(

            "title",

            parent=styles["Normal"],

            alignment=TA_CENTER,

            fontName="Helvetica-Bold",

            fontSize=17,

            leading=17,

            textColor=colors.HexColor("#00c853")
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

        title = Paragraph(
            "EVOPoint",
            title_style
        )

        subtitle = Paragraph(
            "Sistema inteligente de ponto facial",
            subtitle_style
        )

        emitido = Paragraph(

            f"""
            CARTÃO PONTO<br/>
            Emitido em:
            {datetime.now().strftime("%d/%m/%Y %H:%M")}
            """,

            tiny_style
        )

        elements.append(title)
        elements.append(subtitle)
        elements.append(emitido)

        elements.append(
            Spacer(1, 6)
        )

        # =================================================
        # INFO FUNCIONÁRIO
        # =================================================

        if scale:

            seg = (
                f"{scale.entry_1} {scale.exit_1} "
                f"{scale.entry_2} {scale.exit_2}"
                if scale.monday
                else "Folga"
            )

            ter = (
                f"{scale.entry_1} {scale.exit_1} "
                f"{scale.entry_2} {scale.exit_2}"
                if scale.tuesday
                else "Folga"
            )

            qua = (
                f"{scale.entry_1} {scale.exit_1} "
                f"{scale.entry_2} {scale.exit_2}"
                if scale.wednesday
                else "Folga"
            )

            qui = (
                f"{scale.entry_1} {scale.exit_1} "
                f"{scale.entry_2} {scale.exit_2}"
                if scale.thursday
                else "Folga"
            )

            sex = (
                f"{scale.entry_1} {scale.exit_1} "
                f"{scale.entry_2} {scale.exit_2}"
                if scale.friday
                else "Folga"
            )

            sab = (
                f"{scale.entry_1} {scale.exit_1} "
                f"{scale.entry_2} {scale.exit_2}"
                if scale.saturday
                else "Folga"
            )

            dom = (
                f"{scale.entry_1} {scale.exit_1} "
                f"{scale.entry_2} {scale.exit_2}"
                if scale.sunday
                else "Folga"
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

        elements.append(info_table)

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
            "EX100%",
            "BSALDO"
        ]]

        total_normais = 0
        total_faltas = 0
        total_extras = 0
        total_carga = 0

        carga_diaria = parse_schedule(
            employee.schedule
        )

        # =================================================
        # PROCESSA
        # =================================================

        for date, day_records in grouped.items():

            ordered = sorted(

                day_records,

                key=lambda x: x.record_time
            )

            batidas = []

            for r in ordered:

                batidas.append({

                    "time":
                        r.record_time.strftime(
                            "%H:%M"
                        ),

                    "datetime":
                        r.record_time
                })

            while len(batidas) < 6:

                batidas.append(None)

            worked_seconds = 0

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

            faltas = 0
            extras = 0

            if worked_seconds < carga_diaria:

                faltas = (
                    carga_diaria
                    -
                    worked_seconds
                )

            elif worked_seconds > carga_diaria:

                extras = (
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
            total_extras += extras
            total_carga += carga_diaria

            saldo_text = ""

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

            table_data.append([

                datetime.strptime(
                    date,
                    "%Y-%m-%d"
                ).strftime("%d/%m/%Y"),

                batidas[0]["time"] if batidas[0] else "",
                batidas[1]["time"] if batidas[1] else "",

                batidas[2]["time"] if batidas[2] else "",
                batidas[3]["time"] if batidas[3] else "",

                batidas[4]["time"] if batidas[4] else "",
                batidas[5]["time"] if batidas[5] else "",

                seconds_to_hours(
                    worked_seconds
                ),

                seconds_to_hours(
                    faltas
                ),

                seconds_to_hours(
                    extras
                ),

                seconds_to_hours(
                    carga_diaria
                ),

                seconds_to_hours(
                    extras
                ),

                "00:00",

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

        saldo_final_text = ""

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

            "",
            "",

            "",
            "",

            "",
            "",

            seconds_to_hours(
                total_normais
            ),

            seconds_to_hours(
                total_faltas
            ),

            seconds_to_hours(
                total_extras
            ),

            seconds_to_hours(
                total_carga
            ),

            seconds_to_hours(
                total_extras
            ),

            "00:00",

            saldo_final_text
        ])

        # =================================================
        # TABELA STYLE
        # =================================================

        table = Table(

            table_data,

            colWidths=[

                48,

                34,
                34,

                34,
                34,

                34,
                34,

                40,
                40,
                40,
                40,
                36,
                40,
                42
            ]
        )

        table.setStyle(TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#00c853")),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),

            ("FONTSIZE", (0, 0), (-1, -1), 5.4),

            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d2d2d2")),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),

            ("TOPPADDING", (0, 0), (-1, -1), 2),

            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f5f5f5"))
        ]))

        elements.append(table)

        elements.append(
            Spacer(1, 8)
        )

        # =================================================
        # RESUMO
        # =================================================

        resumo = Table([[
            "NORMAIS",
            seconds_to_hours(total_normais),

            "FALTAS",
            seconds_to_hours(total_faltas),

            "EXTRAS",
            seconds_to_hours(total_extras),

            "SALDO",
            saldo_final_text
        ]])

        resumo.setStyle(TableStyle([

            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#00c853")),

            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

            ("FONTSIZE", (0, 0), (-1, -1), 5.8),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#00a844")),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),

            ("TOPPADDING", (0, 0), (-1, -1), 3)
        ]))

        elements.append(resumo)

        elements.append(
            Spacer(1, 16)
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

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

            ("FONTSIZE", (0, 0), (-1, -1), 5.5),

            ("TOPPADDING", (0, 0), (-1, -1), 5)
        ]))

        elements.append(assinatura)

        # =================================================
        # BUILD
        # =================================================

        doc.build(elements)

        return FileResponse(

            path=pdf_path,

            filename=pdf_path,

            media_type="application/pdf"
        )

    except Exception as e:

        print("================================")
        print("ERRO PDF")
        print(str(e))
        print("================================")

        return {

            "success": False,

            "error": str(e)
        }

    finally:

        db.close()