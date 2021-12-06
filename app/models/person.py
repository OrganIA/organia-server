import sqlalchemy as sa
from sqlalchemy import orm
import enum

from sqlalchemy.sql.expression import null

from app import db
from app.helpers.enums import EnumStr
from datetime import datetime


class Person(db.TimedMixin, db.Base):
    class Gender(EnumStr):
        MALE = enum.auto()
        FEMALE = enum.auto()
        OTHER = enum.auto()

    class ABO(EnumStr):
        A = enum.auto()
        B = enum.auto()
        AB = enum.auto()
        O = enum.auto()

    class Rhesus(enum.Enum):
        POSITIVE = '+'
        NEGATIVE = '-'

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

    @property
    def age(self):
        now = datetime.utcnow().date()
        age = now.year - self.birthday.year - \
            ((now.month, now.day) < (self.birthday.month, self.birthday.day))
        return age
