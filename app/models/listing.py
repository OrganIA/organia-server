import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.helpers.enums import EnumStr


class Listing(db.DurationMixin, db.Base):
    class Organ(EnumStr):
        HEART = enum.auto()
        KIDNEY = enum.auto()
        LUNG = enum.auto()

    person_id = sa.Column(sa.ForeignKey('persons.id'))
    notes = sa.Column(sa.String)
    hospital_id = sa.Column(sa.ForeignKey('hospitals.id'))
    donor = sa.Column(sa.Boolean, default=False, nullable=False)
    organ = sa.Column(sa.Enum(Organ))
    isDialyse = sa.Column(sa.Boolean, default=False, nullable=True)
    isRetransplantation = sa.Column(sa.Boolean, default=False, nullable=True)
    startDateDialyse = sa.Column(sa.Date, nullable=True)
    EndDateDialyse = sa.Column(sa.Date, nullable=True)
    ARFDate = sa.Column(sa.Date, nullable=True)
    DateTransplantation = sa.Column(sa.Date, nullable=True)
    ReRegistrationDate = sa.Column(sa.Date, nullable=True)
    A = sa.Column(sa.Integer, default=0, nullable=True)
    B = sa.Column(sa.Integer, default=0, nullable=True)
    DR = sa.Column(sa.Integer, default=0, nullable=True)
    DQ = sa.Column(sa.Integer, default=0, nullable=True)

    person = orm.relationship('Person', backref='listings')
    hospital = orm.relationship('Hospital', backref='listings')
