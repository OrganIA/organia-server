import sqlalchemy as sa
from sqlalchemy import null, orm

from app import db
from app import distance
from app import models

class Hospital(db.IdMixin, db.Base):
    city_id = sa.Column(sa.ForeignKey('cities.id'), nullable=False)
    name = sa.Column(sa.String, nullable=False)
    phone_number = sa.Column(sa.String, nullable=True)
    city = orm.relationship('City', backref='hospitals')

    @property
    def latitude(self):
        position = distance.get_coordinates(self.name)
        latitude = position[0]
        return latitude
    
    @property
    def longitude(self):
        position = distance.get_coordinates(self.name)
        longitude = position[1]
        return longitude
    
    @property
    def patient_number(self):
        patient_number = db.session.query(models.Listing).filter_by(hospital=self).count()
        return patient_number
