from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import HTMLResponse
from loguru import logger

# Initialize FastAPI app
app = FastAPI(
    title="DunamisMax API Playground",
    description="Interactive API testing and learning platform",
    version="1.0.0",
)

# Setup static files and templates
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Configure logging
logger.add(
    "logs/dunamismax.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
)


# Main routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "pages/home.html", {"request": request, "active_page": "home"}
    )


@app.get("/demos", response_class=HTMLResponse)
async def demos(request: Request):
    return templates.TemplateResponse(
        "pages/demos.html", {"request": request, "active_page": "demos"}
    )


@app.get("/tutorials", response_class=HTMLResponse)
async def tutorials(request: Request):
    return templates.TemplateResponse(
        "pages/tutorials.html", {"request": request, "active_page": "tutorials"}
    )


@app.get("/playground", response_class=HTMLResponse)
async def playground(request: Request):
    return templates.TemplateResponse(
        "pages/playground.html", {"request": request, "active_page": "playground"}
    )


# Include API routers - only include websocket for now
from dunamismax.app.api.demo import websocket

# Mount API routers
api_routers = [
    (websocket.router, "/api/demo/websocket"),
    # Comment out until we create these routers
    # (streaming.router, "/api/demo/streaming"),
    # (async_ops.router, "/api/demo/async"),
    # (basics.router, "/api/tutorials/basics"),
    # (validation.router, "/api/tutorials/validation"),
    # (security.router, "/api/tutorials/security"),
    # (experiments.router, "/api/playground")
]

for router, prefix in api_routers:
    app.include_router(router, prefix=prefix)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
