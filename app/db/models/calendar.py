import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class CalendarEvent(db.CreatedMixin, db.Base):
    date = sa.Column(sa.DateTime)
    description = sa.Column(sa.String)
    author_id = sa.Column(sa.ForeignKey('users.id'))

    author = orm.relationship('User', backref='calendar_events')
