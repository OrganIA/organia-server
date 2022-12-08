import sqlalchemy as sa
from sqlalchemy import orm

from app.utils import str_format


class Base:
    __AUTO_DICT__ = True
    __AUTO_DICT_EXCLUDE__ = []
    __AUTO_DICT_INCLUDE__ = []

    @orm.declared_attr
    def __tablename__(cls):
        name = cls.__name__
        name = str_format.pluralize(name)
        name = str_format.snake_case(name)
        return name

    id = sa.Column(sa.Integer, primary_key=True)

    def __repr__(self) -> str:
        state = sa.inspect(self)

        if state.transient:
            pk = f"(transient {id(self)})"
        elif state.pending:
            pk = f"(pending {id(self)})"
        else:
            pk = ", ".join(map(str, state.identity))

        return f"<{type(self).__name__} {pk}>"

    def to_dict(self):
        if not self.__AUTO_DICT__:
            raise NotImplementedError
        inst = sa.inspect(self)
        tab = {
            c.key: getattr(self, c.key)
            for c in inst.mapper.column_attrs
            if c.key not in self.__AUTO_DICT_EXCLUDE__
        }
        for key in self.__AUTO_DICT_INCLUDE__:
            if hasattr(self, key):
                tab[key] = getattr(self, key)
        return tab

    def read_dict(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
