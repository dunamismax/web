from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from .agents import AgentManager, available_agents
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="DunamisMax AI Agents")

# Mount static files
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)

# Templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

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
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = available_agents[agent_id]
    return templates.TemplateResponse("chat.html", {"request": request, "agent": agent})


@app.websocket("/ws/chat/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    """WebSocket endpoint for agent chat"""
    try:
        await agent_manager.connect(websocket, agent_id)
    except Exception as e:
        print(f"Connection error: {e}")
        return

    try:
        while True:
            message = await websocket.receive_text()
            await agent_manager.get_agent_response(agent_id, message, websocket)
    except WebSocketDisconnect:
        await agent_manager.disconnect(websocket)
    except Exception as e:
        print(f"Error in websocket: {e}")
        await agent_manager.disconnect(websocket)
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except:
            pass


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8200))
    debug = os.getenv("DEBUG", "False").lower() == "true"

    uvicorn.run("app.main:app", host=host, port=port, reload=debug)
