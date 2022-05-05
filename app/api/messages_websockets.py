from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.encoders import jsonable_encoder
from json import loads
from typing import List

from app import db
from app.models import Message, ChatGroup
from app.api.schemas.messages import MessageCreateSchema, MessageSchema
from app.errors import InvalidRequest, NotFoundError, Unauthorized
from app.utils import websocket_manager

router = APIRouter(prefix='/chats/ws')


manager = websocket_manager.ConnectionManager()


@router.websocket('/{chat_id}')
async def websocket_route(chat_id: int, websocket: WebSocket):
    print('Accepting client connection...')
    await manager.connect(websocket)
    while True:
        try:
            data = loads(await websocket.receive_text())
            if "event" not in data:
                await websocket.send_json({
                    "status": 404,
                    "message": "No protocol found."
                })
                continue
            if data["event"] == "login":
                if "token" not in data:
                    raise Unauthorized("No Bearer token given.")
                manager.get_client(websocket).login(data["token"], chat_id)
                if not check_if_user_in_chat(
                    get_all_users_in_chat(chat_id),
                    manager.get_client(websocket).get_id()
                ):
                    raise Unauthorized("User is not in chat.")
                await websocket.send_json({
                    "status": 200,
                    "message": "Login successful."
                })
                continue
            if (data["event"] == "send_message"):
                if not manager.get_client(websocket).get_if_logged():
                    raise Unauthorized("You are not logged in.")
                check_message(
                    data,
                    chat_id,
                    manager.get_client(websocket).get_id()
                )
                message = await send_message(
                    chat_id=chat_id,
                    data=data,
                    logged_user=manager.get_client(websocket).logged_user
                )
                message_json = jsonable_encoder(
                    MessageSchema.from_orm(message).dict()
                )
                await websocket.send_json(
                    {
                        "status": 200,
                        "event": "message_sent",
                        "data": message_json
                    })
                await manager.broadcast_json({
                    "status": 200,
                    "event": "message_received",
                    "data": message_json
                }, websocket)
                continue
            raise InvalidRequest("Invalid event.")
        except WebSocketDisconnect:
            is_logged = manager.get_client(websocket).get_if_logged()
            if is_logged:
                client_id = manager.get_client(websocket).get_id()
                manager.disconnect(websocket)
                await manager.broadcast_text(
                    f"Client #{client_id} left the chat", websocket
                )
            else:
                manager.disconnect(websocket)
                await manager.broadcast_text(
                    "Unknown client left the chat", websocket
                )
            break
        except HTTPException as e:
            await websocket.send_json({"status": e.status_code,
                                       "event": "error",
                                       "error": e.detail
                                       })
        except Exception as e:
            await websocket.send_json({"status": 400,
                                       "event": "error",
                                       "error": e.args
                                       })


def check_message(data: MessageCreateSchema, chat_id: int, user_id: int):
    if not all(keys in data for keys in ("chat_id", "content", "sender_id")):
        raise Exception("Missing data.")
    if data["chat_id"] != chat_id:
        raise Exception("Wrong chat_id.")
    if data["sender_id"] != user_id:
        raise Exception("Wrong sender_id.")
    if not check_if_user_in_chat(
            get_all_users_in_chat(chat_id),
            user_id):
        raise Exception("User is not in chat.")
    del data["event"]


def check_if_user_in_chat(chat: List[ChatGroup], user_id: int):
    for item in chat:
        if item.user_id == user_id:
            return True
    return False


def get_all_users_in_chat(chat_id: int):
    return db.session.query(ChatGroup).filter_by(
        chat_id=chat_id
    ).all()


async def send_message(
    chat_id: int,
    data: MessageCreateSchema,
    logged_user=None
):
    chat = db.session.query(ChatGroup).filter_by(
        chat_id=chat_id,
        user_id=logged_user.id
    ).all()
    if not chat:
        raise NotFoundError("No chat found for the user with this id.")
    message = Message.from_data(data)
    if not message:
        raise InvalidRequest()
    db.session.add(message)
    db.session.commit()
    return message
