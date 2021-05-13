from sqlalchemy import orm

from app.helpers import str_format


class Base:
    UPDATERS = {}

    @orm.declared_attr
    def __tablename__(cls):
        return f'{str_format.camel_to_snake(cls.__name__)}s'

    def update(self, data, exclude_unset=True, use_updaters=True):
        from pydantic import BaseModel
        if isinstance(data, BaseModel):
            data = data.dict(exclude_unset=exclude_unset)
        for key, value in data.items():
            if use_updaters and key in self.UPDATERS:
                getattr(self, self.UPDATERS[key])(value)
            else:
                setattr(self, key, value)
