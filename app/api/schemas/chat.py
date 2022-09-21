from typing import List

from app import db
from typing import Optional


class ChatGroupSchema(db.Schema):
    chat_id: int
    users_ids: List[int]
    chat_name: str
    creator_id: Optional[int]


class ChatGroupCreateSchema(db.Schema):
    user_id: int


class ChatGroupsCreateSchema(db.Schema):
    users_ids: List[ChatGroupCreateSchema]
    chat_name: str
    creator_id: Optional[int]


class ChatGroupUpdateSchema(db.Schema):
    users_ids: Optional[List[ChatGroupCreateSchema]]
    chat_name: Optional[str]
