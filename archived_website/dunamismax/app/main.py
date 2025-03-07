import logging
import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Load environment variables early
load_dotenv()

# Define base directory
BASE_DIR = Path(__file__).parent

# Ensure the logs directory exists BEFORE configuring logging
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configure logging: logs will stream to both console and file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "dunamismax.log", mode="a"),
    ],
)
logger = logging.getLogger("DunamisMax")

# Create FastAPI application instance
app = FastAPI(title=os.getenv("APP_NAME", "DunamisMax"))

# Mount static files and configure templates
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Define available services (could also be loaded from a configuration file)
SERVICES = [
    {
        "name": "Messenger",
        "description": "Real-time chat application with WebSocket technology for instant messaging and communication",
        "url": "https://messenger.dunamismax.com",
        "icon": "message-square",
        "features": ["Real-time", "WebSocket", "Instant"],
    },
    {
        "name": "AI Agents",
        "description": "Interactive AI assistants powered by advanced language models for specialized tasks and conversations",
        "url": "https://agents.dunamismax.com",
        "icon": "cpu",
        "features": ["AI", "GPT-4", "Assistance"],
    },
    {
        "name": "File Converter",
        "description": "Professional media conversion tool supporting multiple formats with high-quality output",
        "url": "https://files.dunamismax.com",
        "icon": "file",
        "features": ["FFmpeg", "Audio", "Video"],
    },
    {
        "name": "Notes",
        "description": "Password-protected note-taking application with a Nord design",
        "url": "https://notes.dunamismax.com",
        "icon": "book-open",
        "features": ["Password-protected", "CRUD", "PostgreSQL"],
    },
]


@app.get("/", response_model=None)
async def root(request: Request):
    """Render the main page with available services."""
    try:
        logger.info("Rendering main page")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "services": SERVICES,
                "page_title": "DunamisMax - Modern Web Applications",
                "meta_description": "Suite of professional web applications including real-time messaging, AI agents, file conversion, and notes service",
            },
        )
    except Exception as e:
        logger.error(f"Error rendering main page: {e}", exc_info=True)
        raise


@app.get("/privacy", response_model=None)
async def privacy(request: Request):
    """Render the privacy policy page."""
    try:
        logger.info("Rendering privacy page")
        return templates.TemplateResponse(
            "privacy.html",
            {
                "request": request,
                "page_title": "Privacy Policy - DunamisMax",
            },
        )
    except Exception as e:
        logger.error(f"Error rendering privacy page: {e}", exc_info=True)
        raise


@app.get("/health", response_model=dict)
async def health_check():
    """A simple endpoint for health checking."""
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    """Startup tasks: log the service startup."""
    logger.info("DunamisMax service starting up")
    logger.info("DunamisMax service started successfully")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # Adjust the import string if your module structure changes
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true",
    )
