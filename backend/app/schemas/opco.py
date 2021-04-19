from app.models import Opco
import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Opco(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class OpcoCreate(BaseModel):
    title: str
