import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Hospital(db.IdMixin, db.Base):
    city_id = sa.Column(sa.ForeignKey('cities.id'), nullable=False)
    name = sa.Column(sa.String, nullable=False)

    city = orm.relationship('City', backref='hospitals')
