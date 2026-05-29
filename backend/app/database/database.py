from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/evopoint"

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True
)

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)

Base = declarative_base()