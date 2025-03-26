from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ConnectionManager:

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocker: WebSocket):
        self.active_connections.remove(websocker)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()