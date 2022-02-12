from typing import List

from app import db
from app.api.schemas.user import UserSchema


class ChatGroupSchema(db.Schema):
    chat_id: int
    users_ids: List[int]
    chat_name: str


class ChatGroupCreateSchema(db.Schema):
    user_id: int


class ChatGroupsCreateSchema(db.Schema):
    users_ids: List[ChatGroupCreateSchema]
    chat_name : str
