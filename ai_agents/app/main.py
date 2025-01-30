from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from .agents import AgentManager, available_agents

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
        return {"error": "Agent not found"}, 404

    agent = available_agents[agent_id]
    return templates.TemplateResponse("chat.html", {"request": request, "agent": agent})


@app.websocket("/ws/chat/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    """WebSocket endpoint for agent chat"""
    await agent_manager.connect(websocket, agent_id)
    try:
        while True:
            message = await websocket.receive_text()
            response = await agent_manager.get_agent_response(agent_id, message)
            await websocket.send_json(
                {"type": "message", "role": "assistant", "content": response}
            )
    except WebSocketDisconnect:
        await agent_manager.disconnect(websocket)
    except Exception as e:
        print(f"Error in websocket: {e}")
        await agent_manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8200, reload=True)
