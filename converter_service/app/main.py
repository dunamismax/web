import os
import uuid
import logging
import asyncio
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import uvicorn
from dotenv import load_dotenv
import json

# Configure logging before anything else
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("logs/file-converter.log")],
)
logger = logging.getLogger("DunamisMaxFiles")

# Load environment variables
ENV_PATH = Path("/home/sawyer/github/web/converter_service/.env")
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    logger.warning(f".env file not found at {ENV_PATH}")

# Initialize FastAPI with proper configuration
app = FastAPI(title=os.getenv("APP_NAME", "DunamisMax File Converter"))

# Define base directories - Updated to reflect correct structure
BASE_DIR = Path("/home/sawyer/github/web/converter_service")
APP_DIR = BASE_DIR / "app"
UPLOAD_DIR = APP_DIR / "uploads"
CONVERTED_DIR = APP_DIR / "converted"
STATIC_DIR = APP_DIR / "static"
TEMPLATES_DIR = APP_DIR / "templates"

# Ensure required directories exist with proper permissions
for dir_path in [UPLOAD_DIR, CONVERTED_DIR, STATIC_DIR, TEMPLATES_DIR]:
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        dir_path.chmod(0o755)
        logger.info(f"Ensured directory exists: {dir_path}")
    except Exception as e:
        logger.warning(f"Directory setup warning for {dir_path}: {e}")

# Load allowed formats
ALLOWED_FORMATS = {
    "audio": ["mp3", "wav", "ogg", "flac", "aac", "m4a"],
    "video": ["mp4", "mov", "avi", "mkv", "webm"],
}

# Mount static files and templates - Using correct paths
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Track conversion tasks
conversion_tasks = {}


async def verify_ffmpeg():
    """Verify FFmpeg is installed and accessible"""
    try:
        ffmpeg_path = "/usr/bin/ffmpeg"  # Specify full path
        proc = await asyncio.create_subprocess_exec(
            ffmpeg_path,
            "-version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            logger.warning("FFmpeg check failed but continuing")
            return False
        logger.info("FFmpeg verification successful")
        return True
    except Exception as e:
        logger.warning(f"FFmpeg verification failed but continuing: {e}")
        return False


async def save_upload(file: UploadFile, path: Path):
    """Save uploaded file with proper error handling"""
    try:
        with path.open("wb") as buffer:
            while content := await file.read(1024 * 1024):  # 1MB chunks
                buffer.write(content)
        path.chmod(0o644)
        return True
    except Exception as e:
        logger.error(f"File save failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file")


# Routes
@app.get("/")
async def root(request: Request):
    """Render the main page"""
    return templates.TemplateResponse("files.html", {"request": request})


@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...), output_format: str = Form(...)):
    """Handle file conversion requests"""
    if not file.filename:
        raise HTTPException(400, "No file uploaded")

    try:
        file_ext = Path(file.filename).suffix[1:].lower()
        output_format = output_format.lower()

        # Validate formats
        valid_input = any(file_ext in formats for formats in ALLOWED_FORMATS.values())
        valid_output = any(
            output_format in formats for formats in ALLOWED_FORMATS.values()
        )

        if not valid_input or not valid_output:
            raise HTTPException(400, "Unsupported file format")

        task_id = str(uuid.uuid4())
        base_name = Path(file.filename).stem
        output_filename = f"{base_name}-{output_format}.{output_format}"

        # Save original file
        upload_path = UPLOAD_DIR / f"{task_id}_original.{file_ext}"
        await save_upload(file, upload_path)

        # Create conversion task
        conversion_tasks[task_id] = {
            "status": "queued",
            "original": file.filename,
            "upload_path": upload_path,
            "output_path": CONVERTED_DIR / output_filename,
            "start_time": datetime.now(),
            "error": None,
        }

        # Start conversion process
        asyncio.create_task(process_conversion(task_id))

        return {"task_id": task_id, "download_url": f"/download/{output_filename}"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_conversion(task_id: str):
    """Process the actual file conversion"""
    task = conversion_tasks.get(task_id)
    if not task:
        return

    try:
        task["status"] = "processing"

        cmd = [
            "/usr/bin/ffmpeg",
            "-y",
            "-i",
            str(task["upload_path"]),
            str(task["output_path"]),
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {stderr.decode().strip()}")

        task["status"] = "completed"
        logger.info(f"Conversion successful for task {task_id}")

    except Exception as e:
        task["status"] = "failed"
        task["error"] = str(e)
        logger.error(f"Conversion failed for task {task_id}: {e}")
    finally:
        # Cleanup
        try:
            if task["upload_path"].exists():
                task["upload_path"].unlink()
        except Exception as e:
            logger.error(f"Cleanup error for task {task_id}: {e}")


@app.get("/api/conversion-status/{task_id}")
async def conversion_status(task_id: str):
    """Get the status of a conversion task"""
    task = conversion_tasks.get(task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    return {
        "status": task["status"],
        "download_url": (
            f"/download/{task['output_path'].name}"
            if task["status"] == "completed"
            else None
        ),
        "error": task["error"],
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Handle file downloads"""
    try:
        file_path = CONVERTED_DIR / filename
        if not file_path.exists():
            raise HTTPException(404, "File not found")

        return FileResponse(
            file_path, media_type="application/octet-stream", filename=filename
        )
    except Exception as e:
        logger.error(f"Download failed for {filename}: {e}")
        raise HTTPException(500, "File download error")


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    try:
        # Verify FFmpeg but don't fail if not found
        ffmpeg_available = await verify_ffmpeg()
        if not ffmpeg_available:
            logger.warning("FFmpeg not found - conversions will fail")

        logger.info("Startup complete")
    except Exception as e:
        logger.error(f"Startup warning: {e}")


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8300))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    uvicorn.run("main:app", host=host, port=port, reload=debug, log_level="info")
