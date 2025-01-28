from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from pathlib import Path
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="DunamisMax", description="API Playground and Blog", version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Setup logging
logger.add(
    "logs/app.log", rotation="500 MB", retention="10 days", level="INFO", serialize=True
)

# Active WebSocket connections for messenger
active_connections: list[WebSocket] = []


# Base context for all templates
def get_base_context(request: Request):
    return {"request": request, "current_year": datetime.now().year}


@app.get("/")
async def home(request: Request):
    """Render the home page."""
    context = get_base_context(request)
    return templates.TemplateResponse("pages/home.html", context)


@app.get("/blog")
async def blog(request: Request):
    """Render the blog page."""
    context = get_base_context(request)
    return templates.TemplateResponse("pages/blog.html", context)


@app.get("/about")
async def about(request: Request):
    """Render the about page."""
    context = get_base_context(request)
    return templates.TemplateResponse("pages/about.html", context)


@app.get("/playground")
async def playground(request: Request):
    """Render the API playground page."""
    context = get_base_context(request)
    return templates.TemplateResponse("pages/playground.html", context)


@app.get("/messenger")
async def messenger(request: Request):
    """Render the messenger page."""
    context = get_base_context(request)
    return templates.TemplateResponse("pages/messenger.html", context)


@app.websocket("/ws/messenger")
async def messenger_endpoint(websocket: WebSocket):
    """WebSocket endpoint for the messenger feature."""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast message to all connected clients
            for connection in active_connections:
                await connection.send_text(data)
    except Exception as e:
        logger.exception(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)


# Import and include routers
from app.api import blog, messenger, playground

app.include_router(blog.router, prefix="/api/blog", tags=["blog"])
app.include_router(messenger.router, prefix="/api/messenger", tags=["messenger"])
app.include_router(playground.router, prefix="/api/playground", tags=["playground"])
