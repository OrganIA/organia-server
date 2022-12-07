import enum

import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.utils.enums import EnumStr


class Listing(db.Base):
    __AUTO_DICT_EXCLUDE__ = ['person_id']
    __AUTO_DICT_INCLUDE__ = ['person', 'lung', 'liver']

    class Type(EnumStr):
        DONOR = enum.auto()
        RECEIVER = enum.auto()

    class Organ(EnumStr):
        HEART = enum.auto()
        KIDNEY = enum.auto()
        LUNG = enum.auto()
        LIVER = enum.auto()

    # fields

    notes = sa.Column(sa.String)
    type = sa.Column(sa.Enum(Type))

    @property
    def organ(self):
        return self.liver or self.lung

    person_id = sa.Column(sa.ForeignKey('persons.id'))
    hospital_id = sa.Column(sa.ForeignKey('hospitals.id'))

    person = orm.relationship(
        'Person', backref='listings', cascade='all,delete'
    )
    hospital = orm.relationship('Hospital', backref='listings')
    liver = orm.relationship(
        'Liver',
        back_populates='listing',
        cascade='all,delete',
        uselist=False,
    )
    lung = orm.relationship(
        'Lung', back_populates='listing', cascade='all, delete', uselist=False
    )
