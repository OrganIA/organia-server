import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_utils import PhoneNumberType
from werkzeug import security

from app import db
from app.db.mixins import TimedMixin
from app.errors import AlreadyTakenError, InvalidRequest, PasswordMismatchError


class User(TimedMixin, db.Base):
    """An entity that can login into the platform"""

    email = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String)
    is_admin = sa.Column(sa.Boolean, default=False)
    firstname = sa.Column('first_name', sa.String)
    lastname = sa.Column('last_name', sa.String)
    phone_number = sa.Column(PhoneNumberType)
    role_id = sa.Column(sa.ForeignKey('roles.id'), nullable=False, default=1)

    person = orm.relationship('Person', uselist=False, back_populates='user')
    created_chats = orm.relationship('Chat', back_populates='creator')
    chats = orm.relationship(
        'Chat', secondary='chat_members', back_populates='users'
    )
    messages = orm.relationship('Message', back_populates='sender')
    role = orm.relationship('Role', back_populates='users')

    # TODO: Use getter/setter for password instead of save_password

    def __init__(self, **kwargs):
        if password := kwargs.pop('password', None):
            self.save_password(password)
        super().__init__(**kwargs)

    @classmethod
    @property
    def admin(cls):
        action = db.session.get_or_create(
            cls, filter_cols=['email'], email='admin@localhost', is_admin=True
        )
        if action.created:
            db.session.commit()
        return action.obj

    @classmethod
    def check_email(cls, value, obj=None):
        if not value:
            raise InvalidRequest('Email is required')
        if not value.count('@') == 1:
            raise InvalidRequest('Email is not valid')
        query = db.session.query(cls).filter(cls.email == value)
        if obj and obj.id:
            query = query.filter(cls.id != obj.id)
        if query.count():
            raise AlreadyTakenError('email', value)

        return value

    def save_password(self, value):
        self.password = security.generate_password_hash(value)

    def check_password(self, password, exc=True):
        if not self.password:
            raise InvalidRequest('User has no password')
        result = security.check_password_hash(self.password, password)
        if not result and exc:
            raise exc if isinstance(exc, Exception) else PasswordMismatchError
        return result
