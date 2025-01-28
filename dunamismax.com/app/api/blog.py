from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/blog", response_class=HTMLResponse)
@logger.catch
async def show_blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})
