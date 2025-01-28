# app/main.py
import uvicorn
from fastapi import FastAPI
from loguru import logger

from .api import main_routes, blog, contact, message_board
from .db.database import create_pool, close_pool
from .db.queries import CREATE_CONTACT_TABLE
from .config import DATABASE_URL  # Import the config


def create_app() -> FastAPI:
    """
    Initialize and return the FastAPI application.
    """
    app = FastAPI(title="dunamismax.com", docs_url="/docs", redoc_url="/redoc")

    app.include_router(main_routes.router)
    app.include_router(blog.router)
    app.include_router(message_board.router)
    app.include_router(contact.router)

    return app


app = create_app()


@app.on_event("startup")
@logger.catch
async def startup():
    """
    Starts up the application:
    1) Create asyncpg pool.
    2) Create contacts table if not exists.
    """
    app.state.pool = await create_pool()
    async with app.state.pool.acquire() as conn:
        await conn.execute(CREATE_CONTACT_TABLE)


@app.on_event("shutdown")
@logger.catch
async def shutdown():
    """
    Shuts down the application by closing the pool.
    """
    await close_pool(app.state.pool)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
