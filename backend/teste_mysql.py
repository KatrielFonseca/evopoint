from datetime import datetime

from app.database.database import SessionLocal
from app.models.time_record import TimeRecord

db = SessionLocal()

try:

    novo = TimeRecord(

        employee_registration="999",

        employee_name="TESTE MYSQL",

        record_time=datetime.now(),

        verification_mode="FACIAL",

        device_event="0"
    )

    db.add(novo)

    db.commit()

    print("SALVO COM SUCESSO")

except Exception as e:

    print("ERRO:")
    print(e)

finally:

    db.close()