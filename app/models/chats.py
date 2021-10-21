import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Chat(db.IdMixin, db.Base):
    user_a_id = sa.Column(sa.ForeignKey('users.id'), nullable=False)
    user_b_id = sa.Column(sa.ForeignKey('users.id'), nullable=False)
    messages = orm.relationship("Message", back_populates="chat")
