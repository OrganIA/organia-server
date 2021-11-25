from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app import db
from app.models import ChatGroup, Message
from app.api.schemas.messages import MessageCreateSchema
from app.errors import InvalidRequest, NotFounderror
from app.utils import websocket_manager
from collections import namedtuple
from json import loads

router = APIRouter(prefix='/chats')


manager = websocket_manager.ConnectionManager()


@router.websocket('/{chat_id}')
async def websocket_routek(chat_id: int, websocket: WebSocket):
    print('Accepting client connection...')
    await manager.connect(websocket)
    try:
        while True:
            data = loads(await websocket.receive_text())
            print('DATA:')
            print(data)
            print('//////////')
            if "code" not in data:
                await websocket.send_json({"status": 404, "message": "No protocol found."})
                continue
            elif (data["code"] == 0):
                if "token" not in data:
                    await websocket.send_json({"status": 401, "message": "No Bearer token given."})
                    continue
                else:
                    manager.get_client(websocket).login(data["token"])
                    await websocket.send_json({"status": 200, "message": "Login successful."})
                    continue
            elif (data["code"] == 1):
                if not manager.get_client(websocket).get_if_logged():
                    await websocket.send_json({"status": 401, "message": "You are not logged in."})
                    continue
                else:
                    await manager.broadcast_json({"status": 200, "message": "Nice cock"}, websocket)
                    continue
            else:
                await websocket.send_json({"error": "Invalid protocol code."})
                continue
    except WebSocketDisconnect:
        is_logged = manager.get_client(websocket).get_if_logged()
        manager.disconnect(websocket)
        if is_logged:
            await manager.broadcast_text(f"Client #{manager.get_client(websocket).getId()} left the chat", websocket)
        else:
            await manager.broadcast_text("Unknown client left the chat", websocket)
    except Exception as e:
        await websocket.send_json({"error": e.args})
    print('Bye..')
    # message_from_data = check_messages(data.copy())
    # print('Message from data:')
    # print(message_from_data)
    # print('//////////')
    # send_message(chat_id=chat_id, data=message_from_data,
    #              logged_user=logged_user)
    # except Exception as e:
    #     print(e.args)
    #     await websocket.send_json({"error": e.args[0]})


def check_messages(data: dict):
    if not all(keys in data for keys in ("chat_id", "content", "token", "sender_id")):
        raise Exception("Missing data")
    token = data["token"]
    data.pop("token", token)
    return namedtuple("MessageCreateSchema", data.keys())(*data.values())


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
        raise NotFounderror("No chat found for the user with this id.")
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
