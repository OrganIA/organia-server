from app import db


class ChatSchema(db.IdMixin.Schema):
    user_a_id: int
    user_b_id: int

    class Config:
        orm_mode = True


class ChatCreateSchema(db.Schema):
    user_a_id: int
    user_b_id: int
