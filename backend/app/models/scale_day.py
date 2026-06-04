from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.database.database import Base


class ScaleDay(Base):

    __tablename__ = "scale_days"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    from sqlalchemy import ForeignKey

    scale_id = Column(
        Integer,
        ForeignKey(
            "scales.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    day_name = Column(
        String(20),
        nullable=False
    )

    entry_1 = Column(
        String(8),
        nullable=True
    )

    exit_1 = Column(
        String(8),
        nullable=True
    )

    entry_2 = Column(
        String(8),
        nullable=True
    )

    exit_2 = Column(
        String(8),
        nullable=True
    )

    entry_3 = Column(
        String(8),
        nullable=True
    )

    exit_3 = Column(
        String(8),
        nullable=True
    )