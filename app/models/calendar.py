import sqlalchemy as sa
from sqlalchemy import false, orm
from app import db


class CalendarEvent(db.CreatedMixin, db.Base):
    start_date = sa.Column(sa.DateTime, nullable=False)
    end_date = sa.Column(sa.DateTime, nullable=False)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String)
    typerdv = sa.Column(sa.String, nullable=False)
    author_id = sa.Column(sa.ForeignKey('users.id'))

    author = orm.relationship('User', backref='calendar_events')
