import sqlalchemy as sa
from sqlalchemy import orm

from app import db


class Chat(db.mixins.TimedMixin, db.Base):
    chat_name = sa.Column(
        sa.String, default="Nouvelle conversation", nullable=False
    )
    creator_id = sa.Column(sa.ForeignKey('users.id'))

    creator = orm.relationship("User", back_populates="chats")
    groups = orm.relationship("ChatGroup", back_populates="chat")
    messages = orm.relationship("Message", back_populates="chat")

    def to_dict(self):
        return {
            "id": self.id,
            "chat_name": self.chat_name,
            "creator_id": self.creator_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
