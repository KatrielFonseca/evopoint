from fastapi import APIRouter

from app.devices_evo.commands import EvoCommands

router = APIRouter()

@router.get("/test-evo")
def test_evo():

    evo = EvoCommands(
        ip="192.168.88.9",
        password="1234"
    )

    return evo.device_info()