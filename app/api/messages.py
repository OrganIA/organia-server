from typing import List
from fastapi import APIRouter

from app import db
from app.errors import NotFoundError, Unauthorized, InvalidRequest
from app.models import Chat, Message, ChatGroup
from app.api.schemas.chat import ChatCreateSchema, ChatGroupSchema
from app.api.schemas.messages import MessageSchema, MessageCreateSchema
from .dependencies import logged_user


router = APIRouter(prefix='/chats')


@router.get('/', response_model=List[ChatGroupSchema])
async def get_chats_of_user(logged_user=logged_user):
    chat_group = db.session.query(ChatGroup).filter_by(
        user_id=logged_user.id).all()
    item_list = []
    for group in chat_group:
        tmp_list = db.session.query(ChatGroup).filter_by(
            chat_id=group.chat_id).all()
        user_list = []
        for users in tmp_list:
            user_list.append(users.user_id)
        item_list.append({
            "chat_id": group.chat_id,
            "users": user_list
        })
    return item_list


@router.get('/{chat_id}', response_model=ChatGroupSchema)
async def get_chat_by_id(chat_id: int, logged_user=logged_user):
    chat = db.session.query(ChatGroup).filter_by(
        chat_id=chat_id, user_id=logged_user.id).all()
    if not chat:
        raise NotFoundError("No chat found for the user with this id.")
    group = db.session.query(ChatGroup).filter_by(chat_id=chat_id).all()
    user_list = []
    for elem in group:
        user_list.append(elem.user_id)
    result = {
        "chat_id": group[0].chat_id,
        "users": user_list
    }
    return result


@router.post('/', status_code=201, response_model=ChatGroupSchema)
async def create_chat(data: ChatCreateSchema, logged_user=logged_user):
    found = False
    for elem in data.users_ids:
        if elem.user_id == logged_user.id:
            found = True
            break
    if not found:
        raise InvalidRequest(msg="Cannot create a chat for other users.")
    chat = Chat()
    db.session.add(chat)
    db.session.commit()
    item_list = {"chat_id": chat.id, "users": []}
    for i in data.users_ids:
        item = ChatGroup.from_data(i)
        item.chat_id = chat.id
        item_list["users"].append(item.user_id)
        db.session.add(item)
    db.session.commit()
    return item_list


@router.get('/messages/{chat_id}', response_model=List[MessageSchema])
async def get_messages_of_chat(chat_id: int, logged_user=logged_user):
    chat = db.session.query(ChatGroup).filter_by(
        chat_id=chat_id, user_id=logged_user.id).all()
    if not chat:
        raise NotFoundError("No chat found for the user with this id.")
    return db.session.query(Message).filter_by(chat_id=chat_id).all()


@router.post('/messages/{chat_id}', response_model=MessageSchema)
async def send_message(chat_id: int,
                       data: MessageCreateSchema,
                       logged_user=logged_user
                       ):
    chat = db.session.query(ChatGroup).filter_by(
        chat_id=chat_id, user_id=logged_user.id).all()
    if not chat:
        raise NotFoundError("No chat found for the user with this id.")
    message = Message.from_data(data)
    if not message:
        raise InvalidRequest()
    db.session.add(message)
    db.session.commit()
    return message
