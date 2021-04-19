import datetime

from pydantic import BaseModel

class ReportBase(BaseModel):
    date: datetime.date
    time: datetime.time
    rx: int
    tx: int


class ReportFile(ReportBase):
    opco: str


class Report(ReportBase):
    id: int
    opco: str

    class Config:
        orm_mode = True
