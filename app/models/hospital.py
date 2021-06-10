import sqlalchemy as sa

from app import db


class Hospital(db.IdMixin, db.Base):
    name = sa.Column(sa.String)
