from typing import List
from fastapi import APIRouter, WebSocket

from app import db
from app.api.schemas.messages import MessageCreateSchema
# from .dependencies import websocket_logged_user
from json import loads
from collections import namedtuple
from .messages import send_message

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
            print(data)
            message_from_data = check_messages(data)
            print(message_from_data)
            await send_message(chat_id, data, logged_user=await websocket_logged_user(data["token"]))
        except Exception as e:
            await websocket.send_json({"error": e.args})
    print('Bye..')


def check_messages(data: dict):
    if not all(keys in data for keys in ("chat", "content", "token", "sender")):
        raise Exception("Missing data")
    token = data["token"]
    data.pop("token", token)
    return namedtuple("MessageCreateSchema", data.keys())(*data.values())


async def websocket_logged_user(authorization: str = None):
    if config.FORCE_LOGIN:
        from app.models import Role, User
        return db.get_or_create(
            User,
            search_keys={'role': Role.get_admin_role()},
            create_keys={'email': 'admin@admin'},
        )

    if authorization is None:
        raise InvalidAuthToken('Missing Authorization header')
    PREFIX = 'Bearer '
    authorization.startswith(PREFIX) or InvalidAuthToken.r(
        f'Malformed token, does not start with prefix "{PREFIX}"'
    )
    token = LoginToken.get_from_token(authorization[len(PREFIX):])
    return token.user
