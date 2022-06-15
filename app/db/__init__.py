from flask import g
import sqlalchemy as sa
from sqlalchemy import orm, MetaData
from werkzeug.local import LocalProxy

from app import app, config
from .base import Base as Base_


meta = MetaData(naming_convention={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
})


Base: Base_ = orm.declarative_base(cls=Base_, metadata=meta)


engine = None
Session = None


def setup_db(url=None):
    global engine, Session
    url = url or config.DB_URL
    engine = sa.create_engine(url, echo=config.LOG_SQL, connect_args={'check_same_thread': False})
    Session = orm.sessionmaker(bind=engine, autoflush=False)


setup_db()


def get_session():
    if 'db' not in g:
        g.db = Session()
    return g.db


session = LocalProxy(get_session)


def _close_session():
    if 'db' in g:
        g.db.close()
        g.db = None


@app.before_request
def setup_connection():
    _close_session()
    g.db = Session()


@app.after_request
def close_connection(response):
    _close_session()
    return response


from .actions import add, commit, delete, edit, get, get_or_create, log, Action
from .mixins import CreatedMixin, DurationMixin, IdMixin, TimedMixin
