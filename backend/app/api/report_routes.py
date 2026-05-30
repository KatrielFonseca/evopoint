from fastapi import APIRouter
from fastapi.responses import FileResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from app.database.database import SessionLocal
from app.models.employee import Employee

router = APIRouter()


@router.get("/reports/employees")


@router.get("/reports/bank-hours")
def bank_hours_report():

    from app.services.bank_hours_service import (
        calculate_bank_hours
    )

    try:

        data = calculate_bank_hours()

        pdf_path = "bank_hours_report.pdf"

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(

            Paragraph(

                "EVOPoint - Relatório Banco de Horas",

                styles["Title"]

            )

        )

        elements.append(
            Spacer(1, 12)
        )

        table_data = [[

            "Funcionário",

            "Normais",

            "Extras",

            "Faltas",

            "Saldo"

        ]]

        for item in data:

            table_data.append([

                item["name"],

                item["normal_hours"],

                item["extra_hours"],

                item["missing_hours"],

                item["balance"]

            ])

        table = Table(
            table_data
        )

        table.setStyle(TableStyle([

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
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            )

        ]))

        elements.append(
            table
        )

        doc.build(
            elements
        )

        return FileResponse(

            path=pdf_path,

            filename=pdf_path,

            media_type="application/pdf"

        )

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }




@router.get("/reports/extra-hours")
def extra_hours_report():

    from app.services.bank_hours_service import (
        calculate_bank_hours
    )

    try:

        data = calculate_bank_hours()

        pdf_path = "extra_hours_report.pdf"

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(

            Paragraph(

                "EVOPoint - Relatório de Horas Extras",

                styles["Title"]

            )

        )

        elements.append(
            Spacer(1, 12)
        )

        table_data = [[

            "Funcionário",

            "Horas Extras"

        ]]

        for item in data:

            if item["extra_hours"] != "00:00":

                table_data.append([

                    item["name"],

                    item["extra_hours"]

                ])

        table = Table(
            table_data
        )

        table.setStyle(TableStyle([

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
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            )

        ]))

        elements.append(table)

        doc.build(elements)

        return FileResponse(

            path=pdf_path,

            filename=pdf_path,

            media_type="application/pdf"

        )

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }



@router.get("/reports/absences")
def absences_report():

    from app.services.bank_hours_service import (
        calculate_bank_hours
    )

    try:

        data = calculate_bank_hours()

        pdf_path = "absences_report.pdf"

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(

            Paragraph(

                "EVOPoint - Relatório de Faltas",

                styles["Title"]

            )

        )

        elements.append(
            Spacer(1, 12)
        )

        table_data = [[

            "Funcionário",

            "Faltas"

        ]]

        for item in data:

            if item["missing_hours"] != "00:00":

                table_data.append([

                    item["name"],

                    item["missing_hours"]

                ])

        table = Table(
            table_data
        )

        table.setStyle(TableStyle([

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
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            )

        ]))

        elements.append(table)

        doc.build(elements)

        return FileResponse(

            path=pdf_path,

            filename=pdf_path,

            media_type="application/pdf"

        )

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }






def employees_report():

    db = SessionLocal()

    try:

        employees = db.query(Employee).order_by(
            Employee.name.asc()
        ).all()

        pdf_path = "employees_report.pdf"

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "EVOPoint - Relatório de Funcionários",
                styles["Title"]
            )
        )

        elements.append(
            Spacer(1, 12)
        )

        data = [[
            "Matrícula",
            "Nome",
            "CPF",
            "Empresa",
            "Departamento",
            "Cargo",
            "Escala"
        ]]

        for emp in employees:

            data.append([
                str(emp.registration or ""),
                str(emp.name or ""),
                str(emp.cpf or ""),
                str(emp.company or ""),
                str(emp.department or ""),
                str(emp.role or ""),
                str(emp.schedule or "")
            ])

        table = Table(data)

        table.setStyle(TableStyle([

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
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            )

        ]))

        elements.append(table)

        doc.build(elements)

        return FileResponse(
            path=pdf_path,
            filename=pdf_path,
            media_type="application/pdf"
        )

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        db.close()