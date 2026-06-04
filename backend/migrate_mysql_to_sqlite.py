from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.employee import Employee
from app.models.time_record import TimeRecord
from app.models.company import Company
from app.models.scale import Scale
from app.models.scale_day import ScaleDay
from app.models.settings import Settings
from app.models.holiday import Holiday
from app.models.justification import Justification

# MYSQL
mysql_engine = create_engine(
    "mysql+pymysql://root:123456@localhost:3306/evopoint"
)

MySQLSession = sessionmaker(bind=mysql_engine)

# SQLITE
sqlite_engine = create_engine(
    "sqlite:///evopoint.db",
    connect_args={"check_same_thread": False}
)

SQLiteSession = sessionmaker(bind=sqlite_engine)

mysql = MySQLSession()
sqlite = SQLiteSession()

TABELAS = [

    Company,
    Employee,
    Scale,
    ScaleDay,
    Settings,
    Holiday,
    Justification,
    TimeRecord

]

for tabela in TABELAS:

    print(f"Migrando {tabela.__tablename__}")

    registros = mysql.query(
        tabela
    ).all()

    for registro in registros:

        dados = {}

        for coluna in tabela.__table__.columns:

            dados[coluna.name] = getattr(
                registro,
                coluna.name
            )

        sqlite.merge(
            tabela(**dados)
        )

    sqlite.commit()

    print(
        f"{len(registros)} registros copiados"
    )

mysql.close()
sqlite.close()

print()
print("================================")
print("MIGRAÇÃO FINALIZADA")
print("================================")