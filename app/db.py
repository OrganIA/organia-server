from datetime import datetime
from functools import wraps
from typing import Optional
from pydantic import BaseModel as Schema
import sqlalchemy as sa
from sqlalchemy import orm


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


class Base_:
    updaters = {}

    @orm.declared_attr
    def __tablename__(cls):
        return f'{camel_to_snake(cls.__name__)}s'

    @classmethod
    def updater(cls, attribute):
        """Register a method as a setter for use in `Base.update`"""
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                cls.updaters[attribute] = f
                return f(*args, **kwargs)
            return decorated
        return decorator

    def update(self, data, update_schema=False):
        if update_schema:
            data = data.dict(exclude_unset=True)
        for key, value in data.items():
            if key in self.updaters:
                self.updaters[key](self, value)
            else:
                setattr(self, key, value)


def camel_to_snake(s: str) -> str:
    return ''.join([
        f'_{c.lower()}' if c.isupper() else c for c in s
    ]).lstrip('_')


def get_or_404(*args, **kwargs):
    """Calls sqlalchemy.session.get and raises a 404 if nothing is found"""
    from app.errors import NotFoundError
    result = session.get(*args, **kwargs)
    if result is None:
        raise NotFoundError
    return result


Base: Base_ = orm.declarative_base(cls=Base_)
engine = sa.create_engine('sqlite:///./app.db', echo=True)
Session = orm.sessionmaker(bind=engine)
session = Session()
