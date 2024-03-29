import enum
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.db.mixins import TimedMixin
from app.utils.enums import EnumStr


class Person(TimedMixin, db.Base):
    """Represents a physical person, either a patient or a staff member, holds
    information such as name, address, age, gender, etc."""

    __AUTO_DICT_EXCLUDE__ = ['user_id']
    __AUTO_DICT_INCLUDE__ = ['user']

    class Gender(EnumStr):
        MALE = enum.auto()
        FEMALE = enum.auto()
        OTHER = enum.auto()

    class ABO(EnumStr):
        A = enum.auto()
        B = enum.auto()
        AB = enum.auto()
        O = enum.auto()  # noqa capital O

    class Rhesus(enum.Enum):
        POSITIVE = '+'
        NEGATIVE = '-'

    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    birth_date = sa.Column(sa.Date)
    description = sa.Column(sa.String)
    user_id = sa.Column(sa.ForeignKey('users.id'), unique=True)
    gender = sa.Column(sa.Enum(Gender))
    abo = sa.Column(sa.Enum(ABO))
    rhesus = sa.Column(sa.Enum(Rhesus))
    user = orm.relationship('User', uselist=False, back_populates='person')
    staff = orm.relation('Staff', uselist=False, back_populates='person')

    @property
    def age(self):
        now = datetime.utcnow().date()
        aged_this_year = (now.month, now.day) >= (
            self.birth_date.month,
            self.birth_date.day,
        )
        age = now.year - self.birth_date.year - (1 if aged_this_year else 0)
        return age
