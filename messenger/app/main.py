from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="DunamisMax Messenger")

# Mount static files and templates
BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        self.usernames = set()

    async def connect(self, websocket: WebSocket, username: str) -> bool:
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


@app.get("/")
async def root(request: Request):
    """Render the messenger page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/privacy")
async def privacy(request: Request):
    """Render the privacy policy page"""
    return templates.TemplateResponse(
        "privacy.html",
        {
            "request": request,
            "page_title": "Privacy Policy - DunamisMax",
        },
    )


@app.websocket("/ws/chat/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    """WebSocket endpoint for chat"""
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
        print(f"Error in websocket: {e}")
        await manager.disconnect(username)
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except:
            pass


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8100)),
        reload=os.getenv("DEBUG", "false").lower() == "true",
    )
