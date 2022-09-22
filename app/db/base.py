import sqlalchemy as sa
from sqlalchemy import orm

from app.utils import str_format


class Base:
    _KEYS = []

    @orm.declared_attr
    def __tablename__(cls):
        return f'{str_format.camel_to_snake(cls.__name__)}s'

    def __repr__(self):
        if isinstance(self, type):
            class_ = self
        else:
            class_ = type(self)
        header = [class_.__name__]
        if getattr(self, 'id'):
            header.append(f'#{self.id}')
        body = [
            f'{column.name}={getattr(self, column.name)}'
            for column in class_.__table__.columns
            if column.name != 'id'
        ]
        return '<{header}: {body}>'.format(
            header=' '.join(header), body=', '.join(body)
        )

    def dict(self):
        keys = self._KEYS or [
            c.key for c in sa.inspect(self).mapper.column_attrs
        ]
        return {k: getattr(self, k) for k in keys}
