import sqlalchemy as sa
from sqlalchemy import orm

from app import db, distance

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
    def patients_count(self):
        from app.models import Listing
        return db.session.query(Listing).filter_by(hospital=self).count()
