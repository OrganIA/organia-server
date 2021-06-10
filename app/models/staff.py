import sqlalchemy as sa
from sqlalchemy import orm
from app import db

class Staff(db.IdMixin, db.Base):
    """Represents a medical staff"""

    person_id = sa.Column(sa.ForeignKey('persons.id'))
    notes = sa.Column(sa.String)
    hospital_id = sa.Column(sa.ForeignKey('hospitals.id'))

    person = orm.relationship('Person', uselist=False, back_populates='staff')
    hospital = orm.relationship('Hospital', backref='staff')
