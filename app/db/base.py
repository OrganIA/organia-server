from sqlalchemy import orm

from app.helpers import str_format


class Base:
    UPDATERS = {}

    @orm.declared_attr
    def __tablename__(cls):
        return f'{str_format.camel_to_snake(cls.__name__)}s'

    def update(self, data=None, exclude_unset=True, **kwargs):
        if data:
            data = self.unpack_if_schema(data, exclude_unset=exclude_unset)
        else:
            data = {}
        data.update(kwargs)
        data = self.prepare_data(data)
        for key, value in data.items():
            setattr(self, key, value)
        return self

    @classmethod
    def prepare_data(cls, data: dict):
        for key, value in data.items():
            if key in cls.UPDATERS:
                data[key] = getattr(cls, cls.UPDATERS[key])(value)
        return data

    @staticmethod
    def unpack_if_schema(data, exclude_unset=True) -> dict:
        from pydantic import BaseModel
        if isinstance(data, BaseModel):
            data = data.dict(exclude_unset=exclude_unset)
        return data

    @classmethod
    def from_data(cls, data, exclude_unset=True, use_updaters=True):
        data = cls.unpack_if_schema(data, exclude_unset=exclude_unset)
        if use_updaters:
            data = cls.prepare_data(data)
        return cls(**data)
