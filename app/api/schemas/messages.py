from app import db


class MessageSchema(db.IdMixin.Schema):
    sender: int
    chat: int
    content: str

    class Config:
        orm_mode = True


class MessageCreateSchema(db.Schema):
    sender: int
    chat: int
    content: str
