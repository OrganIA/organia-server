import sqlalchemy as sa

from app import db


class Hospital(db.IdMixin, db.Base):
    department = sa.Column(sa.Integer)
    city = sa.Column(sa.String, nullable=False)
    name = sa.Column(sa.String, nullable=False)
