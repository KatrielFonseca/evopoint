from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import ForeignKey

from app.database.database import Base


class Justification(Base):

    __tablename__ = "justifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id")
    )

    start_date = Column(
        Date
    )

    end_date = Column(
        Date
    )

    justification_type = Column(
        String(100)
    )

    description = Column(
        String(500)
    )

    attachment = Column(
        String(500)
    )