import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.db.mixins import TimedMixin


class Liver(TimedMixin, db.Base):
    listing_id = sa.Column(sa.ForeignKey('listings.id'))
    tumors_number = sa.Column(sa.Integer, default=0)
    biggest_tumor_size = sa.Column(sa.Integer)
    alpha_fetoprotein = sa.Column(sa.Integer)
    listing = orm.relationship('Listing', back_populates='liver', uselist=False)
