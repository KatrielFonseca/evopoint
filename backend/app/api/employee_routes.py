from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.models.employee import Employee

from app.schemas.employee_schema import EmployeeCreate

from app.devices_evo.commands import EvoCommands

from app.models.settings import Settings


router = APIRouter()



# =====================================================
# REALTIME VERSION
# =====================================================

def bump_system_version(db):

    settings = db.query(
        Settings
    ).first()

    if not settings:

        settings = Settings()

        settings.system_version = 1

        db.add(settings)

    else:

        settings.system_version = (
            settings.system_version or 1
        ) + 1





# =====================================================
# LISTAR FUNCIONÁRIOS
# =====================================================

@router.get("/employees")
def list_employees():

    db: Session = SessionLocal()

    try:

        employees = db.query(Employee).order_by(
            Employee.id.asc()
        ).all()

        result = []

        for emp in employees:

            result.append({

                "id": emp.id,

                "registration": str(
                    emp.registration
                ),

                "name": emp.name or "",

                "cpf": emp.cpf or "",

                "company": emp.company or "",

                "department": emp.department or "",

                "role": emp.role or "",

                "whatsapp": emp.whatsapp or "",

                "schedule": emp.schedule or ""

                
            })

        return result

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:

        db.close()

# =====================================================
# GERAR MATRÍCULA ÚNICA
# =====================================================

def generate_registration(db):

    try:

        employees = db.query(Employee).all()

        if not employees:

            return "1000"

        maior = 999

        for emp in employees:

            try:

                numero = int(
                    emp.registration
                )

                if numero > maior:

                    maior = numero

            except:
                pass

        return str(maior + 1)

    except:

        return "1000"

# =====================================================
# CADASTRAR FUNCIONÁRIO
# =====================================================

@router.post("/employees")
def create_employee(employee: EmployeeCreate):

    db: Session = SessionLocal()

    try:

        print("=================================")
        print("CRIANDO FUNCIONÁRIO")
        print("=================================")

        # =====================================
        # GERA MATRÍCULA ÚNICA
        # =====================================

        registration = generate_registration(db)

        print("MATRÍCULA GERADA:")
        print(registration)

        # =====================================
        # VALIDA CPF
        # =====================================

        existing_cpf = db.query(Employee).filter(
            Employee.cpf == employee.cpf
        ).first()

        if existing_cpf:

            return {
                "error": "CPF já cadastrado"
            }

        # =====================================
        # VALIDA MATRÍCULA
        # =====================================

        existing_registration = db.query(Employee).filter(
            Employee.registration == registration
        ).first()

        if existing_registration:

            return {
                "error": "Matrícula duplicada"
            }

        # =====================================
        # MYSQL
        # =====================================

        new_employee = Employee(

            registration=str(registration),

            name=employee.name,

            cpf=employee.cpf,

            company=employee.company,

            department=employee.department,

            role=employee.role,

            whatsapp=employee.whatsapp,

            schedule=employee.schedule

            
        )

        db.add(new_employee)

        bump_system_version(db)

        db.commit()

        db.refresh(new_employee)



        print("MYSQL OK")

        print("ID:")
        print(new_employee.id)

        print("REGISTRATION:")
        print(new_employee.registration)

        # =====================================
        # EVO
        # =====================================

        evo_response = {}

        try:

            settings = db.query(
                Settings
            ).first()

            if not settings:

                raise Exception(
                    "Configurações do EVO não encontradas"
                )

            settings = db.query(
                Settings
            ).first()

            evo = EvoCommands(

                ip=settings.evo_ip,

                password=settings.evo_password
            )

            print("EVO CONECTADO")

            evo_response = evo.create_user(

                enrollid=str(
                    new_employee.registration
                ),

                name=str(
                    employee.name
                ),

                department=str(
                    employee.department
                ),

                password_user="1234",

                admin=0
            )

            print("EVO RESPONSE:")
            print(evo_response)

        except Exception as evo_error:

            print("ERRO EVO:")
            print(str(evo_error))

            evo_response = {
                "error": str(evo_error)
            }

        return {

            "message": "Funcionário criado",

            "id": new_employee.id,

            "registration":
                new_employee.registration,

            "mysql": True,

            "evo_response": evo_response
        }

    except Exception as e:

        db.rollback()

        print("ERRO CREATE:")
        print(str(e))

        return {
            "error": str(e)
        }

    finally:

        db.close()

# =====================================================
# EDITAR FUNCIONÁRIO
# =====================================================

@router.put("/employees/{employee_id}")
def update_employee(

    employee_id: int,

    employee_data: EmployeeCreate
):

    db: Session = SessionLocal()

    try:

        employee = db.query(Employee).filter(
            Employee.id == employee_id
        ).first()

        if not employee:

            return {
                "error": "Funcionário não encontrado"
            }

        # =====================================
        # VALIDA CPF DUPLICADO
        # =====================================

        existing_cpf = db.query(Employee).filter(

            Employee.cpf == employee_data.cpf,

            Employee.id != employee_id

        ).first()

        if existing_cpf:

            return {
                "error": "CPF já cadastrado"
            }

        # =====================================
        # NÃO ALTERA MATRÍCULA
        # =====================================

        employee.name = employee_data.name

        employee.cpf = employee_data.cpf

        employee.company = employee_data.company

        employee.department = employee_data.department

        employee.whatsapp = employee_data.whatsapp

        employee.role = employee_data.role

        employee.schedule = employee_data.schedule

        bump_system_version(db)

        db.commit()

        print("FUNCIONÁRIO ATUALIZADO")

        print("ID:")
        print(employee.id)

        print("REGISTRATION:")
        print(employee.registration)

        return {
            "message": "Funcionário atualizado"
        }

    except Exception as e:

        db.rollback()

        return {
            "error": str(e)
        }

    finally:

        db.close()

# =====================================================
# DELETAR FUNCIONÁRIO
# =====================================================

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    db: Session = SessionLocal()

    try:

        employee = db.query(Employee).filter(
            Employee.id == employee_id
        ).first()

        if not employee:

            return {
                "error": "Funcionário não encontrado"
            }

        print("=================================")
        print("DELETE FUNCIONÁRIO")
        print("=================================")

        print("ID:")
        print(employee.id)

        print("REGISTRATION:")
        print(employee.registration)

        # =====================================
        # EVO DELETE
        # =====================================

        try:

            settings = db.query(
                Settings
            ).first()

            evo = EvoCommands(

                ip=settings.evo_ip,

                password=settings.evo_password
            )

            response = evo.delete_user(

                enrollid=str(
                    employee.registration
                )
            )

            print("DELETE EVO:")
            print(response)

        except Exception as evo_error:

            print("ERRO EVO:")
            print(str(evo_error))

        # =====================================
        # MYSQL DELETE
        # =====================================

        db.delete(employee)

        bump_system_version(db)

        db.commit()

        return {

            "message": "Funcionário deletado"

        }

    except Exception as e:

        db.rollback()

        return {
            "error": str(e)
        }

    finally:

        db.close()