import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app import distance


class Hospital(db.IdMixin, db.Base):
    city_id = sa.Column(sa.ForeignKey('cities.id'), nullable=False)
    name = sa.Column(sa.String, nullable=False)
    latitude = sa.Column(sa.Float, nullable=True)
    longitude = sa.Column(sa.Float, nullable=True)
    city = orm.relationship('City', backref='hospitals')

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