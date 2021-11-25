from typing import List
from fastapi import WebSocket
from app.errors import InvalidAuthToken
from app import config, db
from app.models import LoginToken


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocketClient] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        print("connect here")
        self.active_connections.append(WebSocketClient(websocket=websocket))

    def disconnect(self, websocket: WebSocket):
        for client in self.active_connections:
            if client.websocket == websocket:
                self.active_connections.remove(client)
                break

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_text(self, message: str, websocket: WebSocket):
        for client in self.active_connections:
            if client.websocket != websocket and client.get_if_logged():
                await client.websocket.send_text(message)

    async def broadcast_json(self, message: dict, websocket: WebSocket):
        for client in self.active_connections:
            if client.websocket != websocket and client.get_if_logged() :
                await client.websocket.send_json(message)

    def get_client(self, websocket: WebSocket):
        for client in self.active_connections:
            if client.websocket == websocket:
                return client


class WebSocketClient:
    def __init__(self, websocket):
        self.websocket = websocket
        self.logged_user = None

    def login(self, token):
        self.logged_user = websocket_logged_user(authorization=token)

    def get_id(self):
        if (self.logged_user):
            return self.logged_user.id
        else:
            return ""

    def get_if_logged(self):
        if self.logged_user:
            return True
        else:
            return False


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
