from pydantic import BaseModel

from datetime import date


class JustificationCreate(BaseModel):

    employee_id: int

    start_date: date

    end_date: date

    justification_type: str

    description: str | None = None

    attachment: str | None = None