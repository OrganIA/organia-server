from app import db


class MessageSchema(db.IdMixin.Schema):
    sender_id: int
    chat_id: int
    content: str

    class Config:
        orm_mode = True


class MessageCreateSchema(db.Schema):
    sender_id: int
    chat_id: int
    content: str
