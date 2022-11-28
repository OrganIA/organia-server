import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Staff(db.Base):
    """Represents a medical staff"""

    __tablename__ = 'staff'

    person_id = sa.Column(sa.ForeignKey('persons.id'))
    hospital_id = sa.Column(sa.ForeignKey('hospitals.id'))
    notes = sa.Column(sa.String)

    person = orm.relationship('Person', uselist=False, back_populates='staff')
    hospital = orm.relationship('Hospital', backref='staff')

    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'hospital_id': self.hospital_id,
            'notes': self.notes,
        }
