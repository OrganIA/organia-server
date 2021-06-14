from datetime import datetime, timedelta
from typing import Optional
import sqlalchemy as sa
from sqlalchemy import orm

from app import config, db, security


class Invitation(db.TimedMixin, db.Base):
    user_id = sa.Column(sa.ForeignKey('users.id'), nullable=False)
    consumer_id = sa.Column(sa.ForeignKey('users.id'))
    invite_token = sa.Column('value', sa.String, nullable=False)

    def __str__(self):
        return self.value

    def __init__(self, *args, **kwargs):
        value = kwargs.pop('value', False) or security.generate_token()
        db.Base.__init__(self, *args, **kwargs, invite_token=value)

    def refresh(self):
        self.created_at = datetime.now()

    @property
    def value(self):
        if self.id is None:
            raise Exception(
                'Attempting to return the value of a invitation before committing it'
                '  prevents it from making its value truly unique'
            )
        return f'{self.id}-{self.user_id}-{self.invite_token}'

    @classmethod
    def get_from_invitation(cls, invitation: str):
        id = invitation.split('-')[0]
        try:
            id = int(id)
        except ValueError as e:
            raise Exception('No valid ID found in invitation') from e
        result = db.session.get(cls, id)
        if result.value != invitation:
            raise Exception('Mismatching invitation')
        return result

    @staticmethod
    def get_expiration_date():
        return datetime.now() - timedelta(days=-config.LOGIN_EXPIRATION_DAYS)

    @classmethod
    def clean(cls):
        db.session.query(cls).filter(
            cls.created_at < cls.get_expiration_date()
        ).delete()

    @classmethod
    def get_valid_for_user(cls, user, clean=True, refresh=True):
        """
        clean: Delete all expired invitation (all users)
        reuse: Return an existing invitation instead of creating a new one
        refresh: Refresh the invitation that is reused
        """
        if clean:
            cls.clean()
        result = None
        if refresh:
                result.refresh()

        if not result:
            result = cls(user=user)
        return result

class InvitationSchema(db.TimedMixin.Schema):
    user_id: int
    consumer_id : Optional[int]
    value: str

    class Config:
        orm_mode = True


class InvitationCreateSchema(db.Schema):
    user_id: int
        

    
