from json import loads
from typing import List

from simple_websocket.ws import Server

from app import db, sock
from app.api.chats import MessageCreateSchema
from app.db.models import ChatGroup, Message
from app.errors import (
    HTTPException,
    InvalidRequest,
    NotFoundError,
    Unauthorized,
)
from app.utils import websocket_manager

manager = websocket_manager.ConnectionManager()


@sock.route('/chats/ws/<int:chat_id>')
def websocket_route(websocket: Server, chat_id: int):
    print('Accepting client connection...')
    manager.connect(websocket)
    while websocket.connected:
        try:
            data = loads(websocket.receive())
            if "event" not in data:
                websocket.send({"status": 404, "message": "No protocol found."})
                continue
            elif data["event"] == "login":
                if "token" not in data:
                    raise Unauthorized("No Bearer token given.")
                manager.get_client(websocket).login(data["token"], chat_id)
                if not check_if_user_in_chat(
                    get_all_users_in_chat(chat_id),
                    manager.get_client(websocket).get_id(),
                ):
                    raise Unauthorized("User is not in chat.")
                websocket.send({"status": 200, "message": "Login successful."})
                continue
            if data["event"] == "send_message":
                if not manager.get_client(websocket).get_if_logged():
                    raise Unauthorized("You are not logged in.")
                check_message(
                    data, chat_id, manager.get_client(websocket).get_id()
                )
                message = send_message(
                    chat_id=chat_id,
                    data=data,
                    logged_user=manager.get_client(websocket).user,
                )
                websocket.send(
                    {
                        "status": 200,
                        "event": "message_sent",
                        "data": message.to_dict(),
                    }
                )
                manager.broadcast(
                    {
                        "status": 200,
                        "event": "message_received",
                        "data": message.to_dict(),
                    },
                    websocket,
                )
                continue
            raise InvalidRequest("Invalid event.")
        except HTTPException as e:
            websocket.send(
                {"status": e.code, "event": "error", "error": e.description}
            )
        except Exception as e:
            websocket.send({"status": 400, "event": "error", "error": e.args})


def check_message(data: MessageCreateSchema, chat_id: int, user_id: int):
    if not all(keys in data for keys in ("chat_id", "content", "sender_id")):
        raise Exception("Missing data.")
    if data["chat_id"] != chat_id:
        raise Exception("Wrong chat_id.")
    if data["sender_id"] != user_id:
        raise Exception("Wrong sender_id.")
    if not check_if_user_in_chat(get_all_users_in_chat(chat_id), user_id):
        raise Exception("User is not in chat.")
    del data["event"]


def check_if_user_in_chat(chats: List[ChatGroup], user_id: int):
    for chat in chats:
        if chat.user_id == user_id:
            return True
    return False


def get_all_users_in_chat(chat_id: int):
    return db.session.query(ChatGroup).filter_by(chat_id=chat_id).all()


def send_message(chat_id: int, data: MessageCreateSchema, logged_user=None):
    chat = (
        db.session.query(ChatGroup)
        .filter_by(chat_id=chat_id, user_id=logged_user.id)
        .all()
    )
    if not chat:
        raise NotFoundError("No chat found for the user with this id.")
    print(data)
    message = Message(**data)
    if not message:
        raise InvalidRequest()
    db.session.add(message)
    db.session.commit()
    return message
