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
    staff = orm.relation('Staff', uselist=False, back_populates='person')

    @property
    def blood_type(self):
        if not self.abo or not self.rhesus:
            return None
        return f'{self.abo.name}{self.rhesus.value}'
