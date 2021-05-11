import sqlalchemy as sa
from sqlalchemy import orm
from app import db


class Person(db.TimedMixin, db.Base):
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    birthday = sa.Column(sa.Date, nullable=False)
    description = sa.Column(sa.String)
    supervisor_id = sa.Column(sa.ForeignKey('users.id'), nullable=False)

    supervisor = orm.relationship('User', backref='patients')
