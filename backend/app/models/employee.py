from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date

from app.database.database import Base


class Employee(Base):

    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # IDENTIFICAÇÃO

    registration = Column(String(20))

    name = Column(String(255))

    cpf = Column(String(14))

    pis = Column(String(20))

    rg = Column(String(20))

    # EMPRESA

    company = Column(String(255))

    department = Column(String(255))

    role = Column(String(255))

    schedule = Column(String(255))

    # DATAS

    admission_date = Column(Date)

    dismissal_date = Column(Date)

    # FACIAL

    photo_path = Column(String(500))

    face_embedding = Column(String(5000))

    # STATUS

    active = Column(Boolean, default=True)