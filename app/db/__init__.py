import sqlalchemy as sa
from sqlalchemy import orm

from .base import Base as Base_


Base: Base_ = orm.declarative_base(cls=Base_)
engine = sa.create_engine('sqlite:///./app.db', echo=True)
Session = orm.sessionmaker(bind=engine)
session = Session()

from .helpers import *
from .mixins import Schema, IdMixin, TimedMixin
