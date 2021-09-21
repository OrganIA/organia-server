from app import db


class ChatSchema(db.IdMixin.Schema):
    user_a: int
    user_b: int
    class Config:
        orm_mode = True


class ChatCreateSchema(db.Schema):
    user_a: int
    user_b: int
