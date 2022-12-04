import sqlalchemy as sa
from sqlalchemy import MetaData, orm

from app import config
from app.db.actions.get_or_create import get_or_create as _get_or_create
from app.db.base import Base as Base_

meta = MetaData(
    naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(column_0_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    }
)


engine = sa.create_engine(config.DB_URL, echo=config.LOG_SQL)
session = orm.scoped_session(orm.sessionmaker(bind=engine))
session.get_or_create = lambda *args, **kwargs: _get_or_create(
    *args, session=session, **kwargs
)

Base: Base_ = orm.declarative_base(cls=Base_, metadata=meta)
Base.query = session.query_property()


def init_db():
    from app.db import models as models

    if config.AUTO_CREATE_DB:
        Base.metadata.create_all(engine)


def teardown(exception=None):
    session.remove()
