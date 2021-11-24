from typing import List
from fastapi import APIRouter, WebSocket

from app import config
from app import db
from app.models import LoginToken
from app.api.schemas.messages import MessageCreateSchema
from json import loads
from collections import namedtuple
from app.models import ChatGroup, Message

router = APIRouter(prefix='/chats')


@router.websocket('/{chat_id}')
async def websocket_endpoint(chat_id: int, websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            # Wait for any message from the client
            data = loads(await websocket.receive_text())
            # Send message to the client
            print('DATA:')
            print(data)
            print('//////////')
            message_from_data = check_messages(data.copy())
            print('Message from data:')
            print(message_from_data)
            print('//////////')
            logged_user = await websocket_logged_user(authorization=data["token"])
            send_message(chat_id=chat_id, data=message_from_data,
                         logged_user=logged_user)
        except Exception as e:
            print(e.args)
            await websocket.send_json({"error": e.args})
    print('Bye..')


def check_messages(data: dict):
    if not all(keys in data for keys in ("chat_id", "content", "token", "sender_id")):
        raise Exception("Missing data")
    token = data["token"]
    data.pop("token", token)
    return namedtuple("MessageCreateSchema", data.keys())(*data.values())


async def websocket_logged_user(authorization: str = None):
    print('LOGGED USER')
    if config.FORCE_LOGIN:
        print("t'es dans le if")
        from app.models import Role, User
        return db.get_or_create(
            User,
            search_keys={'role': Role.get_admin_role()},
            create_keys={'email': 'admin@admin'},
        )
    print('1')
    if authorization is None:
        raise InvalidAuthToken('Missing Authorization header')
    print('2')
    PREFIX = 'Bearer '
    print('3')
    authorization.startswith(PREFIX) or InvalidAuthToken.r(
        f'Malformed token, does not start with prefix "{PREFIX}"'
    )
    print('4')
    token = LoginToken.get_from_token(authorization[len(PREFIX):])
    print('5')
    return token.user


def send_message(chat_id: int,
                 data: MessageCreateSchema,
                 logged_user
                 ):
    print("Sending message")
    print(f"chat_id: {chat_id}")
    print(f"user_id: {logged_user.id}")
    chat = db.session.query(ChatGroup).filter_by(
        chat_id=chat_id, user_id=logged_user.id).all()
    print("got chat")
    if not chat:
        print("chat empty")
        raise NotFoundError("No chat found for the user with this id.")
    print("chat not empty")
    print("Data is:")
    print(data)
    print('//////////')
    message = Message.from_data(data)
    print('Message from data 2:')
    print(message)
    print('//////////')
    if not message:
        raise InvalidRequest()
    db.session.add(message)
    db.session.commit()
    return message
