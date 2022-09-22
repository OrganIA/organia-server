import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Hospital(db.IdMixin, db.Base):
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
