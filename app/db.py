from datetime import datetime
from typing import Optional
from pydantic import BaseModel as Schema
import sqlalchemy as sa
from sqlalchemy import orm


def camel_to_snake(s: str) -> str:
    return ''.join([
        f'_{c.lower()}' if c.isupper() else c for c in s
    ]).lstrip('_')


@orm.declarative_mixin
class IdMixin:
    id = sa.Column(sa.Integer, primary_key=True)

    class Schema(Schema):
        id: int


@orm.declarative_mixin
class TimedMixin(IdMixin):
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.utcnow)

    class Schema(IdMixin.Schema):
        created_at: Optional[datetime]
        updated_at: Optional[datetime]


class NamedBase:
    @orm.declared_attr
    def __tablename__(cls):
        return f'{camel_to_snake(cls.__name__)}s'


Base = orm.declarative_base(cls=NamedBase)
engine = sa.create_engine('sqlite:///./app.db', echo=True)
Session = orm.sessionmaker(bind=engine)
session = Session()
