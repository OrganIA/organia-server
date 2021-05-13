from functools import wraps
from sqlalchemy import orm

from app.helpers import str_format


class Base:
    updaters = {}

    @orm.declared_attr
    def __tablename__(cls):
        return f'{str_format.camel_to_snake(cls.__name__)}s'

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

    def update(self, data, update_schema=False, use_updaters=True):
        if update_schema:
            data = data.dict(exclude_unset=True)
        for key, value in data.items():
            if use_updaters and key in self.updaters:
                self.updaters[key](self, value)
            else:
                setattr(self, key, value)
