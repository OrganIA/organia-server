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
    dialyse = sa.Column(sa.Boolean, default=False, nullable=True)
    retransplantation = sa.Column(sa.Boolean, default=False, nullable=True)
    start_date_dialyse = sa.Column(sa.Date, nullable=True)
    end_date_dialyse = sa.Column(sa.Date, nullable=True)
    arf_date = sa.Column(sa.Date, nullable=True)


    person = orm.relationship('Person', backref='listings')
    hospital = orm.relationship('Hospital', backref='listings')
