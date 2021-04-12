from app.models import Opco
import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Opco(BaseModel):
    id: Optional[int] = None
    title: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = False
    is_superuser: bool = False
    full_name: Optional[str] = None
    opco: Optional[Opco] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class Msg(BaseModel):
    msg: str


class ReportBase(BaseModel):
    id: Optional[int] = None
    date: datetime.date
    time: datetime.time
    rx: int
    tx: int


class ReportFile(ReportBase):
    opco: str


class Report(ReportBase):
    opco: Opco

    class Config:
        orm_mode = True
