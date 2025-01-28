from fastapi import APIRouter, File, UploadFile, Form
from pydantic import BaseModel, ValidationError
import json
from datetime import datetime

router = APIRouter()


@router.get("/hello")
async def hello():
    """Simple GET endpoint returning time and greeting"""
    return {"message": "Hello from the API!", "timestamp": datetime.now().isoformat()}


@router.post("/echo")
async def echo(message: str = Form(...)):
    """Echo back the received message with a timestamp"""
    return {"message": message, "timestamp": datetime.now().isoformat(), "echo": True}


class JsonData(BaseModel):
    name: str
    age: int
    email: str


@router.post("/validate-json")
async def validate_json(json_data: str = Form(...)):
    """Validate JSON data against a Pydantic schema"""
    try:
        data = json.loads(json_data)
        validated_data = JsonData(**data)
        return {"valid": True, "data": validated_data.model_dump()}
    except ValidationError as e:
        return {"valid": False, "errors": e.errors()}
    except json.JSONDecodeError:
        return {"valid": False, "errors": ["Invalid JSON format"]}


@router.get("/weather")
async def get_weather(city: str):
    """Mock weather API"""
    weather_data = {
        "london": {"temp": 15, "condition": "Cloudy", "humidity": 80},
        "paris": {"temp": 18, "condition": "Sunny", "humidity": 65},
        "new-york": {"temp": 22, "condition": "Clear", "humidity": 70},
        "tokyo": {"temp": 25, "condition": "Rainy", "humidity": 85},
    }

    return weather_data.get(city.lower(), {"error": "City not found"})
