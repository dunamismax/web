from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
@logger.catch
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/about", response_class=HTMLResponse)
@logger.catch
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
