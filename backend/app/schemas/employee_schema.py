from datetime import date

from pydantic import BaseModel


class EmployeeCreate(BaseModel):

    name: str

    cpf: str

    pis: str | None = None

    rg: str | None = None

    company: str

    department: str

    role: str

    schedule: str

    admission_date: date | None = None

    whatsapp: str | None = None