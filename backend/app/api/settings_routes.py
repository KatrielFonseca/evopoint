from fastapi import APIRouter

from app.database.database import SessionLocal

from app.models.settings import Settings

from app.schemas.settings_schema import (
    SettingsCreate
)

router = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)

# =====================================
# GET SETTINGS
# =====================================

@router.get("/")
def get_settings():

    db = SessionLocal()

    try:

        settings = db.query(
            Settings
        ).first()

        if not settings:

            return {}

        return {

            # EMPRESA

            "company_name":
                settings.company_name,

            "trade_name":
                settings.trade_name,

            "cnpj":
                settings.cnpj,

            "state_registration":
                settings.state_registration,

            "municipal_registration":
                settings.municipal_registration,

            # CONTATO

            "phone":
                settings.phone,

            "email":
                settings.email,

            "responsible":
                settings.responsible,

            # ENDEREÇO

            "address":
                settings.address,

            "number":
                settings.number,

            "district":
                settings.district,

            "city":
                settings.city,

            "state":
                settings.state,

            "zip_code":
                settings.zip_code,

            # EVO

            "evo_ip":
                settings.evo_ip,

            "evo_password":
                settings.evo_password,

            "evo_port":
                settings.evo_port,

            # SERVIDOR

            "server_ip":
                settings.server_ip,

            "server_port":
                settings.server_port

        }

    finally:

        db.close()


# =====================================
# SAVE SETTINGS
# =====================================

@router.post("/")
def save_settings(
    data: SettingsCreate
):

    db = SessionLocal()

    try:

        settings = db.query(
            Settings
        ).first()

        if not settings:

            settings = Settings()

            db.add(settings)

        # EMPRESA

        settings.company_name = (
            data.company_name
        )

        settings.trade_name = (
            data.trade_name
        )

        settings.cnpj = (
            data.cnpj
        )

        settings.state_registration = (
            data.state_registration
        )

        settings.municipal_registration = (
            data.municipal_registration
        )

        # CONTATO

        settings.phone = (
            data.phone
        )

        settings.email = (
            data.email
        )

        settings.responsible = (
            data.responsible
        )

        # ENDEREÇO

        settings.address = (
            data.address
        )

        settings.number = (
            data.number
        )

        settings.district = (
            data.district
        )

        settings.city = (
            data.city
        )

        settings.state = (
            data.state
        )

        settings.zip_code = (
            data.zip_code
        )

        # EVO

        settings.evo_ip = (
            data.evo_ip
        )

        settings.evo_password = (
            data.evo_password
        )

        settings.evo_port = (
            data.evo_port
        )

        # SERVIDOR

        settings.server_ip = (
            data.server_ip
        )

        settings.server_port = (
            data.server_port
        )

        db.commit()

        return {

            "success": True,

            "message":
                "Configurações salvas com sucesso."

        }

    except Exception as e:

        db.rollback()

        return {

            "success": False,

            "error": str(e)

        }

    finally:

        db.close()