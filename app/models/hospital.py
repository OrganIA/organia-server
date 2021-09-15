import sqlalchemy as sa

from app import db


class Hospital(db.IdMixin, db.Base):
    city_id = sa.Column(sa.Integer, nullable=True)
    name = sa.Column(sa.String, nullable=False)
