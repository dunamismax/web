from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/message-board", response_class=HTMLResponse)
@logger.catch
async def show_message_board(request: Request):
    return templates.TemplateResponse("message_board.html", {"request": request})
