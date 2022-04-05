import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app import distance

from app.models import listing

class Hospital(db.IdMixin, db.Base):
    city_id = sa.Column(sa.ForeignKey('cities.id'), nullable=False)
    name = sa.Column(sa.String, nullable=False)
    latitude = sa.Column(sa.Float, nullable=True)
    longitude = sa.Column(sa.Float, nullable=True)
    city = orm.relationship('City', backref='hospitals')
    phone_number = sa.Column(sa.String, nullable=True)
    patient_number = sa.Column(sa.Integer, nullable=True)

    @property
    def get_latitude(self):
        position = distance.get_coordinates(self.name)
        latitude = position[0]
        return latitude
    
    @property
    def get_longitude(self):
        position = distance.get_coordinates(self.name)
        longitude = position[1]
        return longitude
    
    @property
    def number_of_patient(self):
        #get the listing tab
        # patient_number = db.session.query(listing).filter_by(listing.hospital.id).count()
        patient_number = db.session.query(listing).all()
        print(patient_number)
        # We need to get the id of the hospital, then look for all the persons who have his hospital_id, put them in an array then count the number of patient
        # patient_number =  