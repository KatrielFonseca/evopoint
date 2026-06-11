from sqlalchemy import Column, Integer, String, DateTime
from app.database.database import Base

class DeletedLog(Base):

    __tablename__ = "deleted_logs"

    id = Column(Integer, primary_key=True)

    employee_registration = Column(String)

    record_time = Column(DateTime)