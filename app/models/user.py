from passlib.context import CryptContext
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy_utils import PhoneNumber
from typing import Optional

from app import db
from app.errors import AlreadyTakenError, InvalidRequest, PasswordMismatchError
from app.models.chats import Chat


class User(db.TimedMixin, db.Base):
    PASSWORD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
    UPDATERS = {
        'email': 'get_unique_email',
        'password': 'get_hashed_password'
    }

    email = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String, nullable=False)
    firstname = sa.Column(sa.String, nullable=False)
    lastname = sa.Column(sa.String, nullable=False)
    role_id = sa.Column(sa.ForeignKey('roles.id'), nullable=False)
    phone_number = sa.Column(sa.Unicode(20), nullable=False)
    country_code = sa.Column(sa.Unicode(8), nullable=False, default="FR")

    _phone_number = sa.orm.composite(
        PhoneNumber,
        phone_number,
        country_code
    )
    role = orm.relationship('Role', back_populates='users')
    person = orm.relationship('Person', uselist=False, back_populates='user')
    messages = orm.relationship("Message", back_populates="sender")
    groups = orm.relationship("ChatGroup", back_populates="user")

    def __init__(self, *args, **kwargs):
        from .role import Role
        if kwargs.get('role_id'):
            role = db.session.get(Role, kwargs.pop('role_id'))
            if not role:
                raise InvalidRequest()
        elif kwargs.get('role'):
            role = kwargs.pop('role')
            if not role:
                raise InvalidRequest()
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
