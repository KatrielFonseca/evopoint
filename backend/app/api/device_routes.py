from fastapi import APIRouter
from fastapi import Request

from app.devices_evo.commands import EvoCommands

router = APIRouter(
    prefix="/device",
    tags=["Device"]
)

EVO_IP = "192.168.88.9"
EVO_PASSWORD = "1234"


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

    evo = EvoCommands(
        ip=EVO_IP,
        password=EVO_PASSWORD
    )

    return evo.ping()


# =====================================
# INFO
# =====================================

@router.get("/info")
def device_info():

    evo = EvoCommands(
        ip=EVO_IP,
        password=EVO_PASSWORD
    )

    return evo.device_info()


# =====================================
# CAPACIDADE
# =====================================

@router.get("/capacity")
def device_capacity():

    evo = EvoCommands(
        ip=EVO_IP,
        password=EVO_PASSWORD
    )

    return evo.get_capacity()


# =====================================
# SINCRONIZAR HORA
# =====================================

@router.post("/sync-time")
def sync_time():

    evo = EvoCommands(
        ip=EVO_IP,
        password=EVO_PASSWORD
    )

    return evo.sync_time()


# =====================================
# LIMPAR LOGS
# =====================================

@router.post("/clear-logs")
def clear_logs():

    evo = EvoCommands(
        ip=EVO_IP,
        password=EVO_PASSWORD
    )

    return evo.clear_logs()