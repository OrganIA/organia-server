from datetime import date
from typing import Optional

from app import db
from app.models import Person


class PersonSchema(db.Schema):
    first_name: str
    last_name: str
    birthday: date
    description: Optional[str]
    abo: Optional[Person.ABO]
    rhesus: Optional[Person.Rhesus]
    gender: Optional[Person.Gender]

    class Config:
        orm_mode = True


class PersonGetSchema(PersonSchema, db.TimedMixin.Schema):
    blood_type: Optional[str]


class PersonUpdateSchema(PersonSchema):
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[date]
    age: Optional[int]