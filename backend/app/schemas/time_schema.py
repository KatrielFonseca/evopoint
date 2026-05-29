from pydantic import BaseModel
from datetime import datetime


class TimeRecordCreate(BaseModel):

    employee_id: int

    record_time: datetime

    record_type: str


class TimeRecordResponse(BaseModel):

    id: int

    employee_id: int

    record_time: datetime

    record_type: str

    class Config:

        from_attributes = True