from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.database import Base


class Settings(Base):

    __tablename__ = "settings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================
    # EMPRESA
    # =====================================

    company_name = Column(
        String(255)
    )

    trade_name = Column(
        String(255)
    )

    cnpj = Column(
        String(30)
    )

    state_registration = Column(
        String(100)
    )

    municipal_registration = Column(
        String(100)
    )

    # =====================================
    # CONTATO
    # =====================================

    phone = Column(
        String(50)
    )

    email = Column(
        String(255)
    )

    responsible = Column(
        String(255)
    )

    # =====================================
    # ENDEREÇO
    # =====================================

    address = Column(
        String(255)
    )

    number = Column(
        String(20)
    )

    district = Column(
        String(100)
    )

    city = Column(
        String(100)
    )

    state = Column(
        String(50)
    )

    zip_code = Column(
        String(20)
    )

    # =====================================
    # EVO FACIAL
    # =====================================

    evo_ip = Column(
        String(50)
    )

    evo_password = Column(
        String(100)
    )

    evo_port = Column(
        String(20)
    )

    # =====================================
    # SERVIDOR EVPOINT
    # =====================================

    server_ip = Column(
        String(50)
    )

    server_port = Column(
        String(20)
    )
    
    # =====================================
    # REALTIME
    # =====================================

    system_version = Column(
        Integer,
        default=1
    )