from datetime import date
from typing import Optional
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.sql.schema import ForeignKey
from app import db


class Person(db.TimedMixin, db.Base):
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    birthday = sa.Column(sa.Date, nullable=False)
    description = sa.Column(sa.String)
    supervisor_id = sa.Column(sa.ForeignKey('users.id'))

    supervisor = orm.relationship('User', backref='patients')


class PersonSchema(db.TimedMixin.Schema):
    first_name: str
    last_name: str
    birthday: date
    description: Optional[str]
    supervisor_id: Optional[int]

    class Config:
        orm_mode = True


class PersonCreateSchema(db.Schema):
    first_name: str
    last_name: str
    birthday: date
    description: Optional[str]
    supervisor_id: Optional[int]


class PersonUpdateSchema(db.Schema):
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[date]
    description: Optional[str]
