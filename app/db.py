from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm


def camel_to_snake(s: str) -> str:
    return ''.join([
        f'_{c.lower()}' if c.isupper() else c for c in s
    ]).lstrip('_')


@orm.declarative_mixin
class IdMixin:
    id = sa.Column(sa.Integer, primary_key=True)


@orm.declarative_mixin
class TimedMixin(IdMixin):
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.utcnow)


class NamedBase:
    @orm.declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__) + 's'


Base = orm.declarative_base(cls=NamedBase)
engine = sa.create_engine('sqlite:///./app.db', echo=True)
Session = orm.sessionmaker(bind=engine)
session = Session()
