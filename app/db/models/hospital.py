import sqlalchemy as sa
from sqlalchemy import orm

from app import db, geopy


class Hospital(db.Base):
    __AUTO_DICT_EXCLUDE__ = ['city_id']
    __AUTO_DICT_INCLUDE__ = ['city', 'patients_count']

    city_id = sa.Column(sa.ForeignKey('cities.id'), nullable=False)
    name = sa.Column(sa.String, nullable=False)
    phone_number = sa.Column(sa.String)
    latitude = sa.Column(sa.Float)
    longitude = sa.Column(sa.Float)

    city = orm.relationship('City', backref='hospitals', uselist=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.name:
            self.refresh_coordinates()

    def refresh_coordinates(self):
        position = geopy.get_coordinates(self.name)
        if position:
            self.latitude = position[0]
            self.longitude = position[1]

    @property
    def patients_count(self):
        from app.db.models import Listing

        return db.session.query(Listing).filter_by(hospital=self).count()
