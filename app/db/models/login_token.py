from datetime import datetime, timedelta
import sqlalchemy as sa
from sqlalchemy import orm

from app import config, db, security
from app.errors import InvalidAuthToken


class LoginToken(db.TimedMixin, db.Base):
    user_id = sa.Column(sa.ForeignKey('users.id'))
    _value = sa.Column('value', sa.String)

    user = orm.relationship('User', backref='login_tokens')

    def __str__(self):
        return self.value

    def __init__(self, *args, value=None, **kwargs):
        value = value or security.generate_token()
        db.Base.__init__(self, *args, **kwargs, _value=value)

    def refresh(self):
        self.created_at = datetime.utcnow()

    @property
    def value(self):
        if self.id is None:
            raise Exception(
                'Attempting to return the value of a token before committing it'
                '  prevents it from making its value truly unique'
            )
        return f'{self.id}-{self.user_id}-{self._value}'

    @classmethod
    def get_from_token(cls, token: str):
        id = token.split('-')[0]
        try:
            id = int(id)
        except ValueError as e:
            raise InvalidAuthToken('Malformed token, ID field is corrupted') from e
        result = db.session.get(cls, id)
        if not result:
            raise InvalidAuthToken('No token exist for this token ID')
        if result.value != token:
            raise InvalidAuthToken('Mismatching token value')
        return result

    @staticmethod
    def get_expiration_date():
        return datetime.utcnow() - timedelta(days=-config.LOGIN_EXPIRATION_DAYS)

    @classmethod
    def clean(cls):
        db.session.query(cls).filter(
            cls.created_at < cls.get_expiration_date()
        ).delete()

    @classmethod
    def get_valid_for_user(cls, user, clean=False, reuse=True, refresh=True):
        """
        :param clean: Delete all expired tokens (all users)
        :param reuse: Return an existing token instead of creating a new one
        :param refresh: Refresh the token that is reused

        > Why do we re-use tokens?
        Issuing new tokens for each new login only really makes sense if you
        want to track the different login locations of a user. So you can allow
        them to revoke a current session for example. We do not have this kind
        of feature, so by re-using tokens we save on database usage.
        We can however allow an user to disconnect from every locations by
        clearing all of their associated tokens, if they think their account is
        compromised.
        """
        if clean:
            cls.clean()
        result = None
        if reuse:
            result = db.session.query(cls).filter(
                (cls.user == user)
                & (cls.created_at >= cls.get_expiration_date())
            ).first()
            if result and refresh:
                result.refresh()
        if not result:
            result = cls(user=user)
        return result
