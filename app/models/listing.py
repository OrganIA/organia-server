import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.helpers.enums import EnumStr


class Listing(db.DurationMixin, db.Base):
    class Organ(EnumStr):
        HEART = enum.auto()

    person_id = sa.Column(sa.ForeignKey('persons.id'))
    notes = sa.Column(sa.String)
    hospital_id = sa.Column(sa.ForeignKey('hospitals.id'))
    donor = sa.Column(sa.Boolean, default=False, nullable=False)
    tumors_number = sa.Column(sa.Integer, default=0, nullable=False)
    biggest_tumor_size = sa.Column(sa.Integer, nullable=True)
    alpha_fetoprotein = sa.Column(sa.Integer, nullable=True)
    organ = sa.Column(sa.Enum(Organ))

    person = orm.relationship('Person', backref='listings')
    hospital = orm.relationship('Hospital', backref='listings')
