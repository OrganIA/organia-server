from simple_websocket.ws import Server

from app.db.models.login_token import LoginToken
from app.db.models.user import User
from app.errors import HTTPException


class WebSocketClient:
    def __init__(self, websocket: Server):
        self.websocket = websocket
        self.user = None
        self.chat_id = None

    def login(self, token: str, chat_id: int) -> None:
        try:
            self.user: User = LoginToken.get_from_token(token).user
            self.chat_id = chat_id
        except HTTPException as e:
            self.websocket.close(reason=e.code, message=e.description)

    def get_id(self) -> int:
        if not self.user:
            return None
        return self.user.id

    def get_if_logged(self) -> bool:
        return self.user is not None
