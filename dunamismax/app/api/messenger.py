from fastapi import APIRouter, WebSocket
from datetime import datetime

router = APIRouter()

# Store active connections
active_connections: list[WebSocket] = []


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Add timestamp to message
            message = {
                "text": data,
                "timestamp": datetime.now().isoformat(),
                "type": "message",
            }
            # Broadcast to all connected clients
            for connection in active_connections:
                await connection.send_json(message)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)


@router.get("/active-count")
async def get_active_connections():
    """Get count of active connections"""
    return {"active_connections": len(active_connections)}
