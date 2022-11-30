from json import loads

from simple_websocket.ws import Server

from app import db, sock
from app.api.chats import MessageCreateSchema, _get_chat
from app.db.models import Message
from app.db.models.chat import Chat
from app.db.models.user import User
from app.errors import HTTPException, InvalidRequest, Unauthorized
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
                    _get_chat(chat_id, manager.get_client(websocket).user),
                    manager.get_client(websocket).get_id(),
                ):
                    raise Unauthorized("User is not in chat.")
                websocket.send({"status": 200, "message": "Login successful."})
                continue
            if data["event"] == "send_message":
                if not manager.get_client(websocket).get_if_logged():
                    raise Unauthorized("You are not logged in.")
                check_message(data, chat_id, manager.get_client(websocket).user)
                message = send_message(
                    chat_id=chat_id,
                    data=data,
                    user=manager.get_client(websocket).user,
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


def check_message(data: MessageCreateSchema, chat_id: int, user: User):
    if not ("content" in data):
        raise Exception("Missing data.")
    if not check_if_user_in_chat(
        _get_chat(
            chat_id,
        ),
        user.id,
    ):
        raise Exception("User is not in chat.")
    del data["event"]


def check_if_user_in_chat(chat: Chat, user_id: int):
    if user_id in [user.id for user in chat.users]:
        return True
    else:
        return False


def send_message(chat_id: int, data: MessageCreateSchema, user=None):
    chat = _get_chat(chat_id, user)
    message = Message(content=data.content, chat=chat, sender=user)
    if not message:
        raise InvalidRequest()
    db.session.add(message)
    db.session.commit()
    return message
