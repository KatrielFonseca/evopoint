from pydantic import BaseModel


class ScaleCreate(BaseModel):

    name: str

    monday: bool = True
    tuesday: bool = True
    wednesday: bool = True
    thursday: bool = True
    friday: bool = True

    saturday: bool = False
    sunday: bool = False

    entry_1: str
    exit_1: str

    entry_2: str
    exit_2: str

    entry_3: str | None = None
    exit_3: str | None = None