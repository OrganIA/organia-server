from app import db


class MessageSchema(db.TimedMixin.Schema):
    sender_id: int
    chat_id: id
    content: str
    class Config:
        orm_mode = True


class MessageCreateSchema(db.Schema):
    sender_id: int
    chat_id: int
    content:str