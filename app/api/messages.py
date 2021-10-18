from typing import List
from fastapi import APIRouter

from app import db
from app.errors import NotFoundError, Unauthorized
from app.models import Chat, Message
from app.api.schemas.chat import ChatSchema, ChatCreateSchema
from app.api.schemas.messages import MessageSchema, MessageCreateSchema
# from . import permissions
from .dependencies import logged_user


router = APIRouter(prefix='/chats')


@router.get('/', response_model=List[ChatSchema])
async def get_chats_of_user(logged_user=logged_user):
    result = db.session.query(Chat).filter_by(user_a_id=logged_user.id).all()
    result += db.session.query(Chat).filter_by(user_b_id=logged_user.id).all()
    return result


@router.get('/{chat_id}', response_model=ChatSchema)
async def get_chat_by_id(chat_id: int, logged_user=logged_user):
    return db.session.get(Chat, chat_id)


@router.get('/messages/{chat_id}', response_model=List[MessageSchema])
async def get_messages_of_chat(chat_id: int, logged_user=logged_user):
    chat = db.session.get(Chat, chat_id)
    if (logged_user.id != chat.user_a_id and logged_user.id != chat.user_a_id):
        raise Unauthorized("You do not have access to this chat.")
    return db.session.query(Message).filter_by(chat_id=chat_id).all()


@router.post('/', status_code=201, response_model=ChatSchema)
async def create_chat(data: ChatCreateSchema, logged_user=logged_user):
    chat = Chat.from_data(data)
    db.session.add(chat)
    db.session.commit()
    return chat


# @router.get('/me', response_model=UserSchema)
# async def get_me(logged_user=logged_user):
#     return logged_user


# @router.get('/{user_id}', response_model=UserSchema)
# async def get_user(user_id: int):
#     return db.session.get(User, user_id) or NotFoundError.r()


# @router.post('/', status_code=201, response_model=UserSchema)
# async def create_user(data: UserCreateSchema):
#     user = User.from_data(data)
#     db.session.add(user)
#     db.session.commit()
#     return user


# @router.post('/{user_id}', response_model=UserSchema)
# async def update_user(
#     user_id: int, data: UserUpdateSchema, logged_user=logged_user
# ):
#     user = await get_user(user_id)
#     permissions.users.can_edit(logged_user, user)
#     user.update(data)
#     db.session.commit()
#     return user


# @router.delete('/{user_id}')
# async def delete_user(user_id: int):
#     user = await get_user(user_id)
#     db.session.delete(user)
#     db.session.commit()
