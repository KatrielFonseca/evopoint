from pydantic import BaseModel

from datetime import date


class HolidayCreate(BaseModel):

    date: date

    description: str