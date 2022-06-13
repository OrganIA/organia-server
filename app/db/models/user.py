from werkzeug import security
import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.errors import AlreadyTakenError, InvalidRequest, PasswordMismatchError


class User(db.TimedMixin, db.Base):
    email = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String)
    role_id = sa.Column(sa.ForeignKey('roles.id'), nullable=False)

    role = orm.relationship('Role', back_populates='users')
    person = orm.relationship('Person', uselist=False, back_populates='user')
    messages = orm.relationship('Message', back_populates='sender')
    groups = orm.relationship('ChatGroup', back_populates='user')

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
        return security.generate_password_hash(value)

    def check_password(self, password, exc=True):
        result = security.check_password_hash(password, self.password)
        if not result and exc:
            raise exc if isinstance(exc, Exception) else PasswordMismatchError
        return result
