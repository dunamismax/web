# app/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Determine the path to the .env file
env_path = Path(__file__).resolve().parent.parent / ".env"

# Load environment variables from the .env file
load_dotenv(dotenv_path=env_path)

# Access environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
