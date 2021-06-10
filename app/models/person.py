from datetime import date
from typing import Optional
import sqlalchemy as sa
from sqlalchemy import orm
import enum

from app import db

class Gender(enum.Enum):
    MALE = enum.auto()
    FEMALE = enum.auto()
    OTHER = enum.auto()


class ABO(enum.Enum):
    A = enum.auto()
    B = enum.auto()
    AB = enum.auto()
    O = enum.auto()


class Rhesus(enum.Enum):
    POSITIVE = '+'
    NEGATIVE = '-'


class Person(db.TimedMixin, db.Base):
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    birthday = sa.Column(sa.Date, nullable=False)
    description = sa.Column(sa.String)
    user_id = sa.Column(sa.ForeignKey('users.id'), unique=True)
    gender = sa.Column(sa.Enum(Gender))
    abo = sa.Column(sa.Enum(ABO))
    rhesus = sa.Column(sa.Enum(Rhesus))

    user = orm.relationship('User', uselist=False, back_populates='person')

    @property
    def blood_type(self):
        if not self.abo or not self.rhesus:
            return None
        return f'{self.abo.name}{self.rhesus.value}'


class PersonSchema(db.TimedMixin.Schema):
    first_name: str
    last_name: str
    birthday: date
    description: Optional[str]
    supervisor_id: Optional[int]

    class Config:
        orm_mode = True


class PersonCreateSchema(db.Schema):
    first_name: str
    last_name: str
    birthday: date
    description: Optional[str]
    supervisor_id: Optional[int]


class PersonUpdateSchema(db.Schema):
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[date]
    description: Optional[str]
