from app.devices.evo.commands import EvoCommands
from app.database.session import SessionLocal
from app.models.employee import Employee


def sync_employee_to_evo(employee_id, device_ip):

    db = SessionLocal()

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    evo = EvoCommands(
        ip=device_ip,
        password="1234"
    )

    result = evo.create_user(
        enrollid=employee.id,
        name=employee.name,
        department=employee.department,
        password_user="1234",
        admin=0
    )

    return result