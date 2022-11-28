import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Hospital(db.Base):
    city_id = sa.Column(sa.ForeignKey('cities.id'), nullable=False)
    name = sa.Column(sa.String, nullable=False)
    phone_number = sa.Column(sa.String)
    latitude = sa.Column(sa.String)
    longitude = sa.Column(sa.String)

    city = orm.relationship('City', backref='hospitals')

    @property
    def patients_count(self):
        from app.db.models import Listing

        return db.session.query(Listing).filter_by(hospital=self).count()

    def to_dict(self):
        return {
            'id': self.id,
            'city_id': self.city_id,
            'name': self.name,
            'phone_number': self.phone_number,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'patients_count': self.patients_count,
        }
