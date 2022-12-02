from typing import List, Union

from simple_websocket.ws import Server

from app.utils.websocket_client import WebSocketClient


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocketClient] = []

    def connect(self, websocket: Server) -> None:
        self.active_connections.append(WebSocketClient(websocket=websocket))

    def disconnect(self, websocket: Server) -> None:
        for client in self.active_connections:
            if client.websocket == websocket:
                self.active_connections.remove(client)
                client.websocket.close()
                break

    def send_client(self, message: Union[str, dict], websocket: Server) -> None:
        websocket.send(message)

    def broadcast(self, message: Union[str, dict], websocket: Server) -> None:
        for client in self.active_connections:
            if (
                client.websocket != websocket
                and client.is_logged()
                and client.chat_id == self.get_client(websocket).chat_id
            ):
                self.send_client(message, client.websocket)

    def get_client(self, websocket: Server) -> WebSocketClient:
        for client in self.active_connections:
            if client.websocket == websocket:
                return client
