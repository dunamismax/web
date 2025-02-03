from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from dotenv import load_dotenv
import os

# Import the new AgentManager and AVAILABLE_AGENTS from your agents module.
from app.agents import AgentManager, AVAILABLE_AGENTS

# Load environment variables
load_dotenv()

app = FastAPI()

# Mount static files and templates
BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Initialize the agent manager
agent_manager = AgentManager()


@app.get("/")
async def root(request: Request):
    """
    Render the main page with available agents.
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "agents": AVAILABLE_AGENTS,
        },
    )


@app.get("/chat/{agent_name}")
async def chat(request: Request, agent_name: str):
    # Normalize the agent name => agent_id
    agent_id = agent_name.strip().lower().replace(" ", "_")

    if agent_id not in AVAILABLE_AGENTS:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "agents": AVAILABLE_AGENTS,
                "error": f"Agent '{agent_name}' not found.",
            },
        )

    agent_data = AVAILABLE_AGENTS[agent_id]

    # Pass a new dictionary with 'id' included
    agent = {
        "id": agent_id,  # <--- This is crucial for the WebSocket URL
        "name": agent_data["name"],
        "description": agent_data["description"],
        "system_prompt": agent_data["system_prompt"],
        # If you have an icon_path or similar, you can add it here:
        # "icon_path": agent_data.get("icon_path", "")
    }

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "agent": agent,  # Our updated dict
        },
    )


@app.get("/privacy")
async def privacy(request: Request):
    """
    Render the privacy policy page.
    """
    return templates.TemplateResponse(
        "privacy.html",
        {
            "request": request,
            "page_title": "Privacy Policy - DunamisMax",
        },
    )


@app.websocket("/ws/chat/{agent_name}")
async def websocket_endpoint(websocket: WebSocket, agent_name: str):
    """
    WebSocket endpoint for agent chat. Accepts a human-readable agent name,
    then normalizes it to the internal key.
    """
    # Normalize the agent_name
    agent_id = agent_name.strip().lower().replace(" ", "_")

    try:
        # Register the websocket connection with the appropriate agent
        await agent_manager.connect(websocket, agent_id)

        while True:
            # Receive the user's message
            message = await websocket.receive_text()
            # Pass the message to the agent manager to get a streamed response
            await agent_manager.get_agent_response(agent_id, message, websocket)

    except WebSocketDisconnect:
        # Cleanly handle disconnection
        await agent_manager.disconnect(websocket)
    except Exception as e:
        # Catch-all for unexpected issues
        print(f"Error in websocket: {e}")
        await agent_manager.disconnect(websocket)


if __name__ == "__main__":
    # Run the server on 0.0.0.0:8200 by default
    uvicorn.run("app.main:app", host="0.0.0.0", port=8200)
