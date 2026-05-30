from fastapi import FastAPI

import threading

from contextlib import asynccontextmanager

# =========================================
# DATABASE
# =========================================

from app.database.database import engine
from app.database.database import Base
from app.models.scale import Scale

# =========================================
# MODELS
# =========================================

from app.models.employee import Employee
from app.models.time_record import TimeRecord


# =========================================
# ROUTES
# =========================================

from app.api.employee_routes import router as employee_router
from app.api.company_routes import router as company_router
from app.api.time_routes import router as time_router
from app.api.device_routes import router as device_router
from app.api.test_evo import router as test_evo_router
from app.api.time_record_routes import router as time_record_router
from app.api.timesheet_routes import router as timesheet_router
from app.api.pdf_routes import router as pdf_router
from app.api.scale_routes import router as scale_router
from app.api.bank_hours_routes import (
    router as bank_hours_router
)

# =========================================
# REALTIME SERVICE
# =========================================

from app.services.realtime_service import (
    start_realtime_capture
)

# =========================================
# LIFESPAN
# =========================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("================================")
    print("INICIANDO REALTIME")
    print("================================")

    realtime_thread = threading.Thread(
        target=start_realtime_capture,
        daemon=True
    )

    realtime_thread.start()

    yield

    print("================================")
    print("FINALIZANDO API")
    print("================================")

# =========================================
# APP
# =========================================

app = FastAPI(
    title="EVOPoint API",
    version="1.0.0",
    lifespan=lifespan
)

# =========================================
# CREATE TABLES
# =========================================

Base.metadata.create_all(bind=engine)

# =========================================
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "message": "EVOPoint API Online"
    }

# =========================================
# ROUTES
# =========================================

app.include_router(employee_router)

app.include_router(company_router)

app.include_router(time_router)

app.include_router(device_router)

app.include_router(test_evo_router)

app.include_router(time_record_router)

app.include_router(timesheet_router)

app.include_router(pdf_router)

app.include_router(scale_router)

app.include_router(
    bank_hours_router
)

# =========================================
# DEBUG
# =========================================

print("================================")
print("TIME RECORD ROUTES IMPORTADO")
print("================================")