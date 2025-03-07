import os
from datetime import datetime
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Load environment variables early
load_dotenv()

app = FastAPI(title="DunamisMax Messenger")

# Define base directory, mount static files, and set up templates
BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ---------------------------
# Connection Manager for Chat
# ---------------------------
class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}
        self.usernames: set[str] = set()

    async def connect(self, websocket: WebSocket, username: str) -> bool:
        """
        Accept the WebSocket connection if the username is not already in use.
        Returns True on success; otherwise, False.
        """
        if username in self.usernames:
            return False
        await websocket.accept()
        self.active_connections[username] = websocket
        self.usernames.add(username)
        await self.broadcast_message(
            {
                "type": "system",
                "text": f"{username} joined the chat",
                "timestamp": datetime.now().isoformat(),
            }
        )
        return True

    async def disconnect(self, username: str) -> None:
        """
        Remove the disconnected username from the active list and broadcast a leave message.
        """
        if username in self.usernames:
            self.usernames.remove(username)
            self.active_connections.pop(username, None)
            await self.broadcast_message(
                {
                    "type": "system",
                    "text": f"{username} left the chat",
                    "timestamp": datetime.now().isoformat(),
                }
            )

    async def broadcast_message(self, message: dict) -> None:
        """
        Broadcast the given message to all connected clients.
        """
        for connection in self.active_connections.values():
            await connection.send_json(message)


# Create a single instance of the connection manager.
manager = ConnectionManager()


# ---------------------------
# HTTP Endpoints
# ---------------------------
@app.get("/")
async def root(request: Request):
    """
    Render the Messenger landing page.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/privacy")
async def privacy(request: Request):
    """
    Render the privacy policy page.
    """
    return templates.TemplateResponse(
        "privacy.html", {"request": request, "page_title": "Privacy Policy - DunamisMax"}
    )


# ---------------------------
# WebSocket Endpoint for Chat
# ---------------------------
@app.websocket("/ws/chat/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    """
    WebSocket endpoint for real-time chat.
    If the username is already taken, the connection is rejected.
    Otherwise, all messages from the client are broadcast to everyone.
    """
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
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except Exception:
            pass


# ---------------------------
# Run the Application
# ---------------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8100)),
        reload=os.getenv("DEBUG", "false").lower() == "true",
    )
