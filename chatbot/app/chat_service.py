# chatbot/app/chat_service.py
from openai import AsyncOpenAI
from typing import Dict, Any
from .config import get_settings
from .logger import setup_logger

logger = setup_logger(__name__)
settings = get_settings()


class ChatService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def get_chat_response(self, message: str, prompt: str) -> Dict[str, Any]:
        """Get response from OpenAI using modern async client."""
        try:
            response = await self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message},
                ],
            )
            return {"content": response.choices[0].message.content, "role": "assistant"}
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
            return {
                "content": "An error occurred while processing your request.",
                "error": True,
            }
