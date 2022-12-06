from simple_websocket.ws import Server

from app.db.models.login_token import LoginToken
from app.db.models.user import User


class WebSocketClient:
    def __init__(self, websocket: Server):
        self.id = id(websocket)
        self.websocket = websocket
        self.user = None
        self.chat_id = None

    def login(self, token: str, chat_id: int) -> None:
        self.user: User = LoginToken.get_from_token(token).user
        self.chat_id = chat_id

    def get_id(self) -> int:
        if not self.user:
            return None
        return self.user.id

    def is_logged(self) -> bool:
        return self.user is not None

    def __str__(self):
        return f"WebSocketClient(user={self.user}, chat_id={self.chat_id})"
