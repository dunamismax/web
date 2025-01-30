from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from .agents import AgentManager, available_agents
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Mount static files and templates
BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Initialize agent manager
agent_manager = AgentManager()


@app.get("/")
async def root(request: Request):
    """Render the main page with available agents"""
    return templates.TemplateResponse(
        "index.html", {"request": request, "agents": available_agents}
    )


@app.get("/chat/{agent_id}")
async def chat(request: Request, agent_id: str):
    """Render the chat interface for a specific agent"""
    if agent_id not in available_agents:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "agents": available_agents,
                "error": "Agent not found",
            },
        )
    agent = available_agents[agent_id]
    return templates.TemplateResponse("chat.html", {"request": request, "agent": agent})


@app.websocket("/ws/chat/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    """WebSocket endpoint for agent chat"""
    try:
        await agent_manager.connect(websocket, agent_id)
        while True:
            message = await websocket.receive_text()
            await agent_manager.get_agent_response(agent_id, message, websocket)
    except WebSocketDisconnect:
        await agent_manager.disconnect(websocket)
    except Exception as e:
        print(f"Error in websocket: {e}")
        await agent_manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8200)
