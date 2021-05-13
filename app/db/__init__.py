import os
import sqlalchemy as sa
from sqlalchemy import orm

from app import config
from .base import Base as Base_


Base: Base_ = orm.declarative_base(cls=Base_)

session = None
engine = None


def setup_db(url=None, force=False):
    global engine, session
    if not force and session is not None:
        return
    url = url or config.DB_URL
    engine = sa.create_engine(url, echo=True)
    Session = orm.sessionmaker(bind=engine)
    session = Session()


setup_db()


from .mixins import Schema, IdMixin, TimedMixin
