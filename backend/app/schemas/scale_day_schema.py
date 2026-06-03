from pydantic import BaseModel


class ScaleDayCreate(BaseModel):

    scale_id: int

    day_name: str

    entry_1: str | None = None
    exit_1: str | None = None

    entry_2: str | None = None
    exit_2: str | None = None

    entry_3: str | None = None
    exit_3: str | None = None