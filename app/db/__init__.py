import os
import sqlalchemy as sa
from sqlalchemy import orm

from .base import Base as Base_


DB_URL = os.environ.get('DB_URL', 'sqlite:///./app.db')

Base: Base_ = orm.declarative_base(cls=Base_)

engine = None
session = None


def setup_db(url=None):
    global engine, session
    url = url or DB_URL
    engine = sa.create_engine(DB_URL, echo=True)
    Session = orm.sessionmaker(bind=engine)
    session = Session()


setup_db()

from .helpers import get_or_404
from .mixins import Schema, IdMixin, TimedMixin
