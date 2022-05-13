from datetime import datetime, timedelta
import sqlalchemy as sa
from sqlalchemy import orm

from app import config, db, security


class Invitation(db.TimedMixin, db.Base):
    author_id = sa.Column(sa.ForeignKey('users.id'), nullable=False)
    consumer_id = sa.Column(sa.ForeignKey('users.id'))
    invite_token = sa.Column('value', sa.String, nullable=False)

    author = orm.relationship(
        'User', uselist=False, backref='invites', foreign_keys=[author_id]
    )
    consumer = orm.relationship(
        'User', uselist=False, foreign_keys=[consumer_id]
    )

    def __str__(self):
        return self.value

    def __init__(self, *args, value=None, **kwargs):
        value = value or security.generate_token()
        super().__init__(*args, **kwargs, invite_token=value)

    def refresh(self):
        self.created_at = datetime.now()

    @property
    def value(self):
        if self.id is None:
            raise Exception(
                'Attempting to return the value of an invitation token before'
                ' committing it prevents it from making its value truly unique'
            )
        return f'{self.id}-{self.invite_token}'

    @classmethod
    def get_from_token(cls, token: str, session=None):
        session = session or db.session
        id = token.split('-')[0]
        try:
            id = int(id)
        except ValueError as e:
            raise Exception('No valid ID found in invitation token') from e
        result = session.get(cls, id)
        if result.value != token:
            raise Exception('Mismatching invitation token')
        return result

    @staticmethod
    def get_expiration_date():
        return datetime.now() - timedelta(days=-config.LOGIN_EXPIRATION_DAYS)

    @classmethod
    def clean(cls):
        db.session.query(cls).filter(
            cls.created_at < cls.get_expiration_date()
        ).delete()
