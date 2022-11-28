import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Message(db.mixins.TimedMixin, db.Base):
    content = sa.Column(sa.String, nullable=False)
    chat_id = sa.Column(sa.ForeignKey('chats.id'))
    sender_id = sa.Column(sa.ForeignKey('users.id'))

    sender = orm.relationship("User", back_populates="messages")
    chat = orm.relationship("Chat", back_populates="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "chat_id": self.chat_id,
            "sender_id": self.sender_id,
            "created_at": self.created_at,
        }
