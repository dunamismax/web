# chatbot/app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8203
    max_websocket_connections: int = 1000
    rate_limit_per_minute: int = 10
    log_level: str = "INFO"
    model_name: str = "gpt-4o"  # Updated valid model name

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
