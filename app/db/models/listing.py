import enum

import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.utils.enums import EnumStr


class Listing(db.Base):
    __AUTO_DICT_EXCLUDE__ = ['person_id', 'hospital_id']
    __AUTO_DICT_INCLUDE__ = ['person', 'organ', 'hospital']

    class Type(EnumStr):
        DONOR = enum.auto()
        RECEIVER = enum.auto()

    class Organ(EnumStr):
        HEART = enum.auto()
        KIDNEY = enum.auto()
        LUNG = enum.auto()
        LIVER = enum.auto()

        @property
        def table(self):
            from app.db.models import Liver, Lung

            return {
                self.LIVER: Liver,
                self.LUNG: Lung,
            }.get(self)

    notes = sa.Column(sa.String)
    type = sa.Column(sa.Enum(Type))
    organ_type = sa.Column(sa.Enum(Organ))
    start_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)

    person_id = sa.Column(sa.ForeignKey('persons.id'))
    hospital_id = sa.Column(sa.ForeignKey('hospitals.id'))

    person = orm.relationship(
        'Person', backref='listings', cascade='all,delete'
    )
    hospital = orm.relationship('Hospital', backref='listings')
    # Use Listing.organ to access the organ
    _liver = orm.relationship(
        'Liver', back_populates='listing', cascade='all,delete', uselist=False
    )
    _lung = orm.relationship(
        'Lung', back_populates='listing', cascade='all,delete', uselist=False
    )

    @property
    def organ(self):
        return self._liver or self._lung

    def read_dict(self, data):
        from app.db.models import Person

        organ_data = data.pop('organ', None)
        organ_type = data.pop('organ_type', self.organ_type)
        person_data = data.pop('person', None)
        if organ_data:
            if self.organ:
                self.organ.read_dict(organ_data)
            if organ_type:
                setattr(
                    self,
                    '_' + organ_type.value.lower(),
                    organ_type.table(**organ_data),
                )
        if person_data:
            if self.person:
                self.person.read_dict(person_data)
            else:
                self.person = Person(**person_data)
        super().read_dict(data)
