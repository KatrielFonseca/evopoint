from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date

from app.database.database import Base


class Holiday(Base):

    __tablename__ = "holidays"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    date = Column(
        Date
    )

    description = Column(
        String(255)
    )