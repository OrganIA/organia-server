import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Role(db.TimedMixin, db.Base):
    _KEYS = ['name', 'id']

    name = sa.Column(sa.String, nullable=False, unique=True)
    can_manage_users = sa.Column(sa.Boolean, default=False, nullable=False)
    can_manage_persons = sa.Column(sa.Boolean, default=False, nullable=False)
    can_manage_roles = sa.Column(sa.Boolean, default=False, nullable=False)
    can_manage_hospitals = sa.Column(sa.Boolean, default=False, nullable=False)
    can_invite = sa.Column(sa.Boolean, default=False, nullable=False)

    users = orm.relationship('User', back_populates='role')

    @classmethod
    @property
    def default(cls):
        return db.get_or_create(Role, name='default')

    @classmethod
    @property
    def admin(cls):
        role = db.get_or_create(Role, name="admin")
        if db.Action.created:
            for column in sa.inspect(role).mapper.column_attrs:
                key = column.key
                if not key.startswith('can_'):
                    continue
                setattr(role, key, True)
        return role
