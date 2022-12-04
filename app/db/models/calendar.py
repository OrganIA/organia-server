import sqlalchemy as sa
from sqlalchemy import orm

from app import db
from app.db.mixins import TimedMixin


class CalendarEvent(TimedMixin, db.Base):
    __AUTO_DICT_EXCLUDE__ = ['author_id']
    __AUTO_DICT_INCLUDE__ = ['author']

    start_date = sa.Column(sa.DateTime, nullable=False)
    end_date = sa.Column(sa.DateTime, nullable=False)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String)
    event_type = sa.Column(sa.String, nullable=False)
    author_id = sa.Column(sa.ForeignKey('users.id'))

    author = orm.relationship('User', back_populates='calendar_events')
