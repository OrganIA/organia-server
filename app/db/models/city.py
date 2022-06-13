import sqlalchemy as sa

from app import db


class City(db.IdMixin, db.Base):
    __tablename__ = 'cities'

    name = sa.Column(sa.String)
    department_code = sa.Column(sa.String)
