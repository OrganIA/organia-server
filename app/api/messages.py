from fastapi import APIRouter
from typing import List

from sqlalchemy import null

from app import db
from app.api.schemas.chat import ChatGroupsCreateSchema, ChatGroupSchema, ChatGroupUpdateSchema
from app.api.schemas.messages import MessageSchema, MessageCreateSchema
from app.errors import NotFoundError, InvalidRequest, Unauthorized
from app.models import Chat, Message, ChatGroup
from .dependencies import logged_user


router = APIRouter(prefix='/chats')


@router.get('/', response_model=List[ChatGroupSchema])
async def get_chats_of_user(logged_user=logged_user):
    chat_group = db.session.query(ChatGroup).filter_by(
        user_id=logged_user.id
    ).all()
    item_list = []
    for group in chat_group:
        tmp_list = db.session.query(ChatGroup).filter_by(
            chat_id=group.chat_id
        ).all()
        tmp_list_chats = db.session.query(Chat).filter_by(
            id=group.chat_id).all()
        user_list = []
        for users in tmp_list:
            user_list.append(users.user_id)
        item_list.append({
            "chat_id": group.chat_id,
            "users_ids": user_list,
            "chat_name": tmp_list_chats[0].chat_name,
            "creator_id": tmp_list_chats[0].creator_id,
        })
    return item_list


@router.get('/{chat_id}', response_model=ChatGroupSchema)
async def get_chat_by_id(chat_id: int, logged_user=logged_user):
    chat_group = db.session.query(ChatGroup).filter_by(
        chat_id=chat_id, user_id=logged_user.id
    ).all()
    if not chat_group:
        raise NotFoundError("No chat found for the user with this id.")
    chat = db.session.query(Chat).filter_by(id=chat_id).all()
    group = db.session.query(ChatGroup).filter_by(chat_id=chat_id).all()
    user_list = []
    for elem in group:
        user_list.append(elem.user_id)
    result = {
        "chat_id": group[0].chat_id,
        "users_ids": user_list,
        "chat_name": chat[0].chat_name,
        "creator_id": chat[0].creator_id
    }
    return result


@router.get('/messages/latest', response_model=List[MessageSchema])
async def get_latest_message_chat(logged_user=logged_user):
    chat_groups = (
        db.session.query(ChatGroup)
        .filter_by(user_id=logged_user.id)
    ).all()
    if not chat_groups:
        return []
    latest_messages = []
    for chat_group in chat_groups:
        message = (
            db.session.query(Message)
            .filter_by(chat_id=chat_group.chat_id)
            .order_by(Message.created_at.desc())
        ).first()
        if message:
            latest_messages.append(message)
    return latest_messages


@router.get('/{chat_id}/messages', response_model=List[MessageSchema])
async def get_messages_of_chat(chat_id: int, logged_user=logged_user):
    chat = db.session.query(ChatGroup).filter_by(
        chat_id=chat_id,
        user_id=logged_user.id
    ).all()
    if not chat:
        raise NotFoundError("No chat found for the user with this id.")
    return db.session.query(Message).filter_by(chat_id=chat_id).all()


@router.post('/', status_code=201, response_model=ChatGroupSchema)
async def create_chat(data: ChatGroupsCreateSchema, logged_user=logged_user):
    if not any(x.user_id == logged_user.id for x in data.users_ids):
        raise InvalidRequest(msg="Cannot create a chat for other users.")
    chat = Chat()
    chat.chat_name = data.chat_name
    chat.creator_id = logged_user.id
    db.session.add(chat)
    db.session.commit()
    item_list = {
        "chat_id": chat.id,
        "users_ids": [],
        "chat_name": data.chat_name,
        "creator_id": chat.creator_id,
    }
    for i in data.users_ids:
        item = ChatGroup.from_data(i)
        item.chat_id = chat.id
        item_list["users_ids"].append(item.user_id)
        db.session.add(item)
    db.session.commit()
    return item_list


@router.post('/{chat_id}', status_code=201, response_model=ChatGroupSchema)
async def update_chat(
        data: ChatGroupUpdateSchema,
        chat_id: int,
        logged_user=logged_user
):
    chat = db.session.query(Chat).filter_by(id=chat_id).all()
    if not chat:
        raise NotFoundError("No chat found for the user with this id.")
    if chat[0].creator_id != logged_user.id:
        raise InvalidRequest(msg="You are not the creator of this chat")
    item_list = {"chat_id": chat_id, "users_ids": [],
                 "chat_name": chat[0].chat_name,
                 "creator_id": chat[0].creator_id}

    if data.users_ids:
        for elem in data.users_ids:
            if elem.user_id == logged_user.id:
                break
        else:
            raise InvalidRequest(msg="Cannot remove the creator from the chat.")

        chat_group = db.session.query(ChatGroup).filter_by(
            chat_id=chat_id).all()

        new_users_list = []
        for user_id in data.users_ids:
            new_users_list.append(user_id.user_id)

        former_users_list = []
        for former_user in chat_group:
            former_users_list.append(former_user.user_id)

        for i in former_users_list:
            if i not in new_users_list:
                db.session.query(ChatGroup).filter_by(
                    chat_id=chat_id, user_id=i).delete()
        db.session.commit()
        for i in data.users_ids:
            if i.user_id not in former_users_list:
                item = ChatGroup.from_data(i)
                item.chat_id = chat_id
                db.session.add(item)

    if data.chat_name:
        setattr(chat[0], 'chat_name', data.chat_name)
        item_list["chat_name"] = data.chat_name
    db.session.commit()

    chat_group = db.session.query(ChatGroup).filter_by(
        chat_id=chat_id).all()
    for chat in chat_group:
        item_list["users_ids"].append(chat.user_id)

    return item_list


@router.delete('/{chat_id}')
async def delete_chat(
        chat_id: int,
        logged_user=logged_user
):
    chats = db.session.query(Chat).filter_by(id=chat_id).first()
    chat_groups = db.session.query(ChatGroup).filter_by(chat_id=chat_id).all()
    if chats and chat_groups:
        if logged_user.id  != chats.creator_id:
            raise Unauthorized("You do not have permissions on this chat")
        for i in chat_groups:
            db.delete(i)
        db.delete(chats)
    else:
        raise NotFoundError("No chat found with this id.")


@router.post('/{chat_id}/messages', response_model=MessageSchema)
async def send_message(
    chat_id: int,
    data: MessageCreateSchema,
    logged_user=logged_user,
):
    chat = db.session.query(ChatGroup).filter_by(
        chat_id=chat_id,
        user_id=logged_user.id
    ).all()
    if not chat:
        raise NotFoundError("No chat found for the user with this id.")
    message = Message.from_data(data)
    if not message:
        raise InvalidRequest
    db.session.add(message)
    db.session.commit()
    return message
