from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class BlogPost(BaseModel):
    title: str
    content: str
    created_at: datetime = datetime.now()


@router.get("/")
async def get_posts():
    """Get all blog posts"""
    # Placeholder - would typically fetch from database
    return {
        "posts": [
            {
                "title": "Getting Started with FastAPI and HTMX",
                "excerpt": "Learn how to build modern web applications...",
                "created_at": "2025-01-28",
            }
        ]
    }


@router.get("/{post_id}")
async def get_post(post_id: str):
    """Get a specific blog post"""
    # Placeholder - would typically fetch from database
    return {
        "title": "Getting Started with FastAPI and HTMX",
        "content": "Full post content here...",
        "created_at": "2025-01-28",
    }
