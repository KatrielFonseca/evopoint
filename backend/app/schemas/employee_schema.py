from pydantic import BaseModel


class EmployeeCreate(BaseModel):

    name: str

    cpf: str

    company: str

    department: str

    role: str

    schedule: str