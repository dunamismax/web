from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn

app = FastAPI(title="DunamisMax")

# Mount static files
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)

# Templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "services": [
                {
                    "name": "Messenger",
                    "description": "Real-time chat application using WebSocket technology",
                    "url": "https://messenger.dunamismax.com",
                    "icon": "message-square",
                },
                {
                    "name": "AI Agents",
                    "description": "Chat with specialized AI personalities and assistants",
                    "url": "https://agents.dunamismax.com",
                    "icon": "cpu",
                },
                # Add more services here as they become available
            ],
        },
    )

    # New section in main.py


@app.get("/files")
async def files_page(request: Request):
    """File conversion landing page"""
    return templates.TemplateResponse("files.html", {"request": request})


@app.post("/api/convert")
async def convert_file(request: Request, file: UploadFile = File(...)):
    """Handle file conversion"""
    return await FileConverterService().handle_conversion(file)


@app.get("/api/conversion-status/{task_id}")
async def check_status(task_id: str):
    """Check conversion task status"""
    return await FileConverterService().get_status(task_id)


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download converted files"""
    return await FileConverterService().serve_file(filename)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
