import sqlalchemy as sa
from sqlalchemy import orm
import enum

from app import db

class Organ(enum.Enum):
    HEART = enum.auto()


class Listing(db.DurationMixin, db.Base):
    person_id = sa.Column(sa.ForeignKey('persons.id'))
    notes = sa.Column(sa.String)
    hospital_id = sa.Column(sa.ForeignKey('hospitals.id'))
    donor = sa.Column(sa.Boolean, default=False, nullable=False)
    organ = sa.Column(sa.Enum(Organ))

    person = orm.relationship('Person', backref='listings')
    hospital = orm.relationship('Hospital', backref='listings')
