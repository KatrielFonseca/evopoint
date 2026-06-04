from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

from app.database.database import Base
from sqlalchemy.orm import relationship


class Scale(Base):

    __tablename__ = "scales"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================
    # IDENTIFICAÇÃO
    # =====================================

    name = Column(
        String(255),
        unique=True
    )

    # =====================================
    # DIAS DA SEMANA
    # =====================================

    monday = Column(
        Boolean,
        default=True
    )

    tuesday = Column(
        Boolean,
        default=True
    )

    wednesday = Column(
        Boolean,
        default=True
    )

    thursday = Column(
        Boolean,
        default=True
    )

    friday = Column(
        Boolean,
        default=True
    )

    saturday = Column(
        Boolean,
        default=False
    )

    sunday = Column(
        Boolean,
        default=False
    )

    # =====================================
    # HORÁRIOS
    # =====================================

    entry_1 = Column(
        String(8)
    )

    exit_1 = Column(
        String(8)
    )

    entry_2 = Column(
        String(8)
    )

    exit_2 = Column(
        String(8)
    )

    entry_3 = Column(
        String(8),
        nullable=True
    )

    exit_3 = Column(
        String(8),
        nullable=True
    )