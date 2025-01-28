from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
from pathlib import Path

from .messenger import router

app = FastAPI(title="DunamisMax Messenger")

# Mount static files
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)

# Templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# Include messenger router
app.include_router(router, prefix="/ws")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8100, reload=True)
