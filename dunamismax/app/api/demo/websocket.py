from fastapi import APIRouter

router = APIRouter(
    tags=["WebSocket Demo"],
    responses={404: {"description": "Not found"}},
)


@router.get("/status")
async def websocket_status():
    return {"status": "WebSocket endpoints initialized"}
