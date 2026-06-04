from fastapi import APIRouter
from fastapi import Request

from app.devices_evo.commands import EvoCommands

from app.database.database import SessionLocal
from app.models.settings import Settings

router = APIRouter(
    prefix="/device",
    tags=["Device"]
)

def get_evo():

    db = SessionLocal()

    try:

        settings = db.query(
            Settings
        ).first()

        if not settings:

            raise Exception(
                "Configurações EVO não encontradas."
            )

        return EvoCommands(

            settings.evo_ip,

            settings.evo_port,

            settings.evo_password

        )

    finally:

        db.close()


# =====================================
# PUSH
# =====================================

@router.post("/push")
async def receive_device_data(request: Request):

    body = await request.body()

    print("\n========== EVENTO DO FACIAL ==========")
    print(body.decode(errors="ignore"))
    print("======================================\n")

    return {
        "status": "ok"
    }


# =====================================
# STATUS
# =====================================

@router.get("/status")
def device_status():

    evo = get_evo()

    return evo.ping()


# =====================================
# INFO
# =====================================

@router.get("/info")
def device_info():

    evo = get_evo()

    return evo.device_info()


# =====================================
# CAPACIDADE
# =====================================

@router.get("/capacity")
def device_capacity():

    evo = get_evo()

    return evo.get_capacity()


# =====================================
# SINCRONIZAR HORA
# =====================================

@router.post("/sync-time")
def sync_time():

    evo = get_evo()

    return evo.sync_time()


# =====================================
# LIMPAR LOGS
# =====================================

@router.post("/clear-logs")
def clear_logs():

    evo = get_evo()

    return evo.clear_logs()