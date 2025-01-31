# chatbot/app/main.py
import time
import json
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException, status, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .config import get_settings
from .logger import setup_logger
from .rate_limiter import RateLimiter
from .chat_service import ChatService

settings = get_settings()
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    logger.info("Starting application...")
    try:
        app.state.rate_limiter = RateLimiter(settings.rate_limit_per_minute)
        app.state.chat_service = ChatService()
        yield
    finally:
        logger.info("Application shutdown complete")


app = FastAPI(
    title="Chatbot API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
)

# Security middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Request logging middleware"""
    start_time = time.monotonic()
    client_ip = request.client.host if request.client else "unknown"

    response = await call_next(request)

    process_time = time.monotonic() - start_time
    logger.info(
        f"{client_ip} - {request.method} {request.url.path} "
        f"-> {response.status_code} ({process_time:.3f}s)"
    )

    return response


@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/chat")
async def chat_endpoint(request: Request, data: Dict = Body(...)):
    """Main chat endpoint"""
    client_ip = request.client.host
    rate_limiter = request.app.state.rate_limiter

    if await rate_limiter.is_rate_limited(client_ip):
        raise HTTPException(
            status_code=429, detail="Rate limit exceeded", headers={"Retry-After": "60"}
        )

    try:
        message = data.get("message")
        prompt = data.get("prompt")

        if not message or not prompt:
            raise HTTPException(status_code=400, detail="Missing required fields")

        return await request.app.state.chat_service.get_chat_response(message, prompt)

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


def main():
    """Entry point for running the application"""
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
