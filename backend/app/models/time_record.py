from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import String

from app.database.database import Base


class TimeRecord(Base):

    __tablename__ = "time_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_registration = Column(
        String(50)
    )

    employee_name = Column(
        String(255)
    )

    record_time = Column(
        DateTime
    )

    verification_mode = Column(
        String(50)
    )

    device_event = Column(
        String(50)
    )

    inout = Column(
        Integer
    )