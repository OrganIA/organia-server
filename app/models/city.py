import sqlalchemy as sa

from app import db

class City(db.IdMixin, db.Base):
    name = sa.Column(sa.String, nullable=True)
    department_code = sa.Column(sa.String, nullable=True)