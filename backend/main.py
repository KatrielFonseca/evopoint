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
from app.models.scale import Scale
from app.models.scale_day import ScaleDay
from app.models.deleted_log import DeletedLog


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
from app.api.report_routes import (
    router as report_router
)

from app.models.settings import Settings
from app.models.holiday import Holiday

from app.api.settings_routes import (
    router as settings_router
)
from app.api.holiday_routes import (
    router as holiday_router
)

from app.api.justification_routes import (
    router as justification_router
)

from app.api.scale_routes import router as scale_router
from app.api.scale_day_routes import (
    router as scale_day_router
)

from app.api.dashboard_routes import (
    router as dashboard_router
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

from sqlalchemy import text

def run_migrations():

    with engine.connect() as conn:

        columns = conn.execute(
            text("PRAGMA table_info(settings)")
        ).fetchall()

        column_names = [
            c[1]
            for c in columns
        ]

        # ====================================
        # last_log_index
        # ====================================

        if "last_log_index" not in column_names:

            print(
                "CRIANDO COLUNA last_log_index..."
            )

            conn.execute(
                text(
                    """
                    ALTER TABLE settings
                    ADD COLUMN last_log_index
                    INTEGER DEFAULT 0
                    """
                )
            )

            conn.commit()

        # ====================================
        # system_version
        # ====================================

        if "system_version" not in column_names:

            print(
                "CRIANDO COLUNA system_version..."
            )

            conn.execute(
                text(
                    """
                    ALTER TABLE settings
                    ADD COLUMN system_version
                    VARCHAR(50)
                    DEFAULT '2.0'
                    """
                )
            )

            conn.commit()

            print(
                "COLUNA system_version CRIADA"
            )

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
    scale_day_router
)

app.include_router(
    bank_hours_router
)
app.include_router(
    report_router
)

app.include_router(
    settings_router
)

app.include_router(
    holiday_router
)

app.include_router(
    justification_router
)

app.include_router(
    dashboard_router
)
# =========================================
# DEBUG
# =========================================

print("================================")
print("TIME RECORD ROUTES IMPORTADO")
print("================================")

# =========================================
# START API
# =========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False
    )