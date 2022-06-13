from werkzeug import security
import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.errors import AlreadyTakenError, PasswordMismatchError


def get_default_role_id():
    from .role import Role
    return Role.default.id


class User(db.TimedMixin, db.Base):
    _KEYS = ['email', 'role']

    email = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String)
    role_id = sa.Column(sa.ForeignKey('roles.id'), nullable=False, default=get_default_role_id)

    role = orm.relationship('Role', back_populates='users')
    person = orm.relationship('Person', uselist=False, back_populates='user')
    messages = orm.relationship('Message', back_populates='sender')
    groups = orm.relationship('ChatGroup', back_populates='user')

    def __init__(self, **kwargs):
        if (password := kwargs.pop('password', None)):
            self.save_password(password)
        super().__init__(**kwargs)

    @classmethod
    @property
    def admin(cls):
        from .role import Role
        user = db.get_or_create(cls, email='admin@localhost')
        if db.Action.created:
            user.role = Role.admin
            db.commit()
        return user

    @classmethod
    def check_email(cls, value, obj=None):
        AlreadyTakenError.check(
            cls, 'email', value,
            filters=cls.id != obj.id if obj else None,
        )
        return value

    def save_password(self, value):
        self.password = security.generate_password_hash(value)

    def check_password(self, password, exc=True):
        result = security.check_password_hash(self.password, password)
        if not result and exc:
            raise exc if isinstance(exc, Exception) else PasswordMismatchError
        return result
