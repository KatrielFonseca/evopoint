from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

import os
import sys

# =========================================
# PASTA DO EXECUTÁVEL
# =========================================

if getattr(sys, "frozen", False):

    BASE_DIR = os.path.dirname(
        sys.executable
    )

else:

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

DB_PATH = os.path.join(
    BASE_DIR,
    "evopoint.db"
)

print("================================")
print("BANCO SQLITE:")
print(DB_PATH)
print("================================")

DATABASE_URL = f"sqlite:///{DB_PATH}"

# =========================================
# ENGINE
# =========================================

engine = create_engine(

    DATABASE_URL,

    connect_args={
        "check_same_thread": False
    }
)

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)

Base = declarative_base()