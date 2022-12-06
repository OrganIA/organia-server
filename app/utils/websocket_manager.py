import logging
from typing import List

from simple_websocket.ws import Server

from app.utils.websocket_client import WebSocketClient


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocketClient] = []

    def connect(self, websocket: Server) -> None:
        self.active_connections.append(WebSocketClient(websocket=websocket))

    def disconnect(self, websocket: Server) -> None:
        logging.warn(f"Disconnecting client {id(websocket)}")
        for client in self.active_connections:
            logging.warn(f"Client: {client.id}")
            logging.warn(
                f"Websocket: {client.websocket.environ['REMOTE_ADDR']}"
            )
            if client.id != id(websocket):
                continue
            logging.critical("Removing client")
            self.active_connections.remove(client)
            client.websocket.close()

    def send_client(self, message: str, client: WebSocketClient) -> None:
        client.websocket.send(message)

    def broadcast(self, message: str, client: WebSocketClient) -> None:
        for cl in self.active_connections:
            if (
                cl.user.id != client.user.id
                and cl.is_logged()
                and cl.chat_id == client.chat_id
            ):
                self.send_client(message, cl)

    def get_client(self, websocket: Server) -> WebSocketClient:
        for client in self.active_connections:
            if client.id == id(websocket):
                return client
