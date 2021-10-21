from app import db
from app.api.schemas.user import UserSchema


class ChatSchema(db.IdMixin.Schema):
    user_a: UserSchema
    user_b: UserSchema

    class Config:
        orm_mode = True


class ChatCreateSchema(db.Schema):
    user_a_id: int
    user_b_id: int
