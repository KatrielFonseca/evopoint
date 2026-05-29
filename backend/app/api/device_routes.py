from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/device",
    tags=["Device"]
)

@router.post("/push")
async def receive_device_data(request: Request):

    body = await request.body()

    print("\n========== EVENTO DO FACIAL ==========")
    print(body.decode(errors="ignore"))
    print("======================================\n")

    return {
        "status": "ok"
    }