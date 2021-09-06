import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Hospital(db.IdMixin, db.Base):
    department = sa.Column(sa.Integer)
    city = sa.Column(sa.String, nullable=False)
    h_name = sa.Column(sa.String, nullable=False)
