import asyncio
from fastapi import WebSocket

from app.schemas.websocket import MessageWS


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    def add_task(self, message: MessageWS):
        asyncio.run(self.broadcast(message=message))

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: MessageWS):
        for connection in self.active_connections:
            await connection.send_json(message.json())


manager = ConnectionManager()
