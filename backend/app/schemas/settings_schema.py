from pydantic import BaseModel


class SettingsCreate(BaseModel):

    # EMPRESA

    company_name: str | None = None

    trade_name: str | None = None

    cnpj: str | None = None

    state_registration: str | None = None

    municipal_registration: str | None = None

    # CONTATO

    phone: str | None = None

    email: str | None = None

    responsible: str | None = None

    # ENDEREÇO

    address: str | None = None

    number: str | None = None

    district: str | None = None

    city: str | None = None

    state: str | None = None

    zip_code: str | None = None

    # EVO

    evo_ip: str | None = None

    evo_password: str | None = None

    evo_port: str | None = None

    # SERVIDOR

    server_ip: str | None = None

    server_port: str | None = None