from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime
from typing import Dict, List

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.usernames: List[str] = []

    async def connect(self, websocket: WebSocket, username: str) -> bool:
        if username in self.usernames:
            return False
        await websocket.accept()
        self.active_connections[username] = websocket
        self.usernames.append(username)
        await self.broadcast_message(
            {
                "type": "system",
                "text": f"{username} joined the chat",
                "timestamp": datetime.now().isoformat(),
            }
        )
        return True

    async def disconnect(self, username: str):
        if username in self.usernames:
            self.usernames.remove(username)
            del self.active_connections[username]
            await self.broadcast_message(
                {
                    "type": "system",
                    "text": f"{username} left the chat",
                    "timestamp": datetime.now().isoformat(),
                }
            )

    async def broadcast_message(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)


manager = ConnectionManager()


@router.websocket("/chat/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    success = await manager.connect(websocket, username)
    if not success:
        await websocket.close(code=1008, reason="Username already taken")
        return

    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "type": "message",
                "username": username,
                "text": data,
                "timestamp": datetime.now().isoformat(),
            }
            await manager.broadcast_message(message)
    except WebSocketDisconnect:
        await manager.disconnect(username)
    except Exception as e:
        print(f"WebSocket error: {e}")
        await manager.disconnect(username)
