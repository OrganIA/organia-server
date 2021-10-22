from app import db
from app.api.schemas.user import UserSchema
from typing import List


class ChatGroupSchema(db.Schema):
    chat_id: int
    users: List[int]


class ChatGroupCreateSchema(db.Schema):
    user_id: int


class ChatCreateSchema(db.Schema):
    users_ids: List[ChatGroupCreateSchema]
