from datetime import date
from typing import Optional

from app import db


class PersonSchema(db.TimedMixin.Schema):
    first_name: str
    last_name: str
    birthday: date
    description: Optional[str]

    class Config:
        orm_mode = True


class PersonCreateSchema(db.Schema):
    first_name: str
    last_name: str
    birthday: date
    description: Optional[str]


class PersonUpdateSchema(db.Schema):
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[date]
    description: Optional[str]
