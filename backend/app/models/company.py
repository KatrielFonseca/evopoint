from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.database import Base


class Company(Base):

    __tablename__ = "companies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        unique=True
    )

    cnpj = Column(
        String(20)
    )

    address = Column(
        String(255)
    )