from typing import Optional
import sqlalchemy as sa
from sqlalchemy import orm
from passlib.context import CryptContext

from app import db
from app.errors import AlreadyTakenError, PasswordMismatchError


class User(db.TimedMixin, db.Base):
    PASSWORD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
    UPDATERS = {
        'email': 'get_unique_email',
        'password': 'get_hashed_password'
    }

    email = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String)
    role_id = sa.Column(sa.ForeignKey('roles.id'), nullable=False)

    role = orm.relationship('Role', back_populates='users')
    person = orm.relationship('Person', uselist=False, back_populates='user')

    def __init__(self, *args, **kwargs):
        from .role import Role
        if kwargs.get("role_id"):
            role = db.session.get(Role, kwargs["role_id"])
        else:
            role = Role.get_default_role()
        super().__init__(*args, **kwargs, role=role)

    @classmethod
    def get_unique_email(cls, value, obj=None):
        AlreadyTakenError.check(
            cls, 'email', value,
            filters=cls.id != obj.id if obj else None,
        )
        return value

    @classmethod
    def get_hashed_password(cls, value):
        return cls.PASSWORD_CONTEXT.hash(value)

    def check_password(self, password, exc=True):
        result = self.PASSWORD_CONTEXT.verify(password, self.password)
        if not result and exc:
            raise exc if isinstance(exc, Exception) else PasswordMismatchError
        return result
