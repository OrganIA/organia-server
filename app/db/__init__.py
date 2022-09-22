import sqlalchemy as sa
from flask import g
from sqlalchemy import MetaData, orm
from werkzeug.local import LocalProxy

from app import config

from .base import Base as Base_

meta = MetaData(
    naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(column_0_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    }
)


Base: Base_ = orm.declarative_base(cls=Base_, metadata=meta)


engine = None
Session = None


def setup_db(url=None, create_tables=False):
    global engine, Session
    url = url or config.DB_URL
    engine = sa.create_engine(
        url, echo=config.LOG_SQL, connect_args={'check_same_thread': False}
    )
    Session = orm.sessionmaker(bind=engine)

    if create_tables:
        Base.metadata.create_all(engine)


def get_session():
    g.db = Session()
    return g.db


session = LocalProxy(get_session)


def _close_session():
    if 'db' in g:
        g.db.close()
        g.db = None


def before_request():
    _close_session()
    g.db = Session()


def after_request(response):
    _close_session()
    return response


from .actions import get_or_create as get_or_create
from .mixins import CreatedMixin as CreatedMixin
from .mixins import DurationMixin as DurationMixin
from .mixins import IdMixin as IdMixin
from .mixins import TimedMixin as TimedMixin
