from typing import List
from fastapi import APIRouter

from app import db
from app.errors import NotFoundError, Unauthorized, InvalidRequest
from app.models import Chat, Message
from app.api.schemas.chat import ChatSchema, ChatCreateSchema
from app.api.schemas.messages import MessageSchema, MessageCreateSchema
from .dependencies import logged_user


router = APIRouter(prefix='/chats')


@router.get('/', response_model=List[ChatSchema])
async def get_chats_of_user(logged_user=logged_user):
    result = db.session.query(Chat).filter_by(user_a_id=logged_user.id).all()
    result += db.session.query(Chat).filter_by(user_b_id=logged_user.id).all()
    return result


@router.get('/{chat_id}', response_model=ChatSchema)
async def get_chat_by_id(chat_id: int, logged_user=logged_user):
    chat = db.get(Chat, chat_id)
    if not chat:
        raise NotFoundError("No chat found with this id.")
    if logged_user.id not in (chat.user_a_id, chat.user_b_id):
        raise Unauthorized("You do not have access to this chat.")
    return chat


@router.post('/', status_code=201, response_model=ChatSchema)
async def create_chat(data: ChatCreateSchema, logged_user=logged_user):
    chat = Chat.from_data(data)
    if not chat:
        raise InvalidRequest()
    if logged_user.id not in (chat.user_a_id, chat.user_b_id):
        raise InvalidRequest(msg="Cannot create a chat for other users.")
    if db.session.query(Chat).filter_by(
        user_a_id=chat.user_a_id,
        user_b_id=chat.user_b_id
    ).first():
        raise InvalidRequest(msg="A chat between these users alredy exists.")
    db.session.add(chat)
    db.session.commit()
    return chat


@router.get('/messages/{chat_id}', response_model=List[MessageSchema])
async def get_messages_of_chat(chat_id: int, logged_user=logged_user):
    chat = db.get(Chat, chat_id)
    if logged_user.id not in (chat.user_a_id, chat.user_b_id):
        raise Unauthorized("You do not have access to this chat.")
    return db.session.query(Message).filter_by(chat_id=chat_id).all()


@router.post('/messages/{chat_id}', response_model=MessageSchema)
async def send_message(chat_id: int,
                       data: MessageCreateSchema,
                       logged_user=logged_user
                       ):
    chat = db.get(Chat, chat_id)
    if logged_user.id not in (chat.user_a_id, chat.user_b_id):
        raise InvalidRequest(msg="User does not belong to this chat.")
    message = Message.from_data(data)
    if not message:
        raise InvalidRequest()
    db.session.add(message)
    db.session.commit()
    return message
