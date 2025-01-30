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

# Load environment variables from .env
ENV_PATH = "/home/sawyer/github/web/converter_service/.env"
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    logging.warning(f".env file not found at {ENV_PATH}")

# Validate environment variables
app_name = os.getenv("APP_NAME", "DunamisMax File Converter")
allowed_formats_json = os.getenv("ALLOWED_FORMATS")

if not allowed_formats_json:
    logging.error("ALLOWED_FORMATS is missing in the .env file. Using default values.")
    allowed_formats_json = '{"audio":["mp3","wav","ogg","flac","aac","m4a"],"video":["mp4","mov","avi","mkv","webm"]}'

try:
    ALLOWED_FORMATS = json.loads(allowed_formats_json)
except json.JSONDecodeError as e:
    logging.critical(f"Failed to parse ALLOWED_FORMATS: {e}")
    raise RuntimeError("Invalid JSON format in ALLOWED_FORMATS environment variable")

# Configure logging before other imports
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("DunamisMaxFiles")

# Initialize FastAPI
app = FastAPI(title=app_name)

# Explicitly define the base directory
BASE_DIR = Path("/home/sawyer/github/web/converter_service").resolve()
UPLOAD_DIR = BASE_DIR / "uploads"
CONVERTED_DIR = BASE_DIR / "converted"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Ensure required directories exist
for dir_path in [UPLOAD_DIR, CONVERTED_DIR, STATIC_DIR, TEMPLATES_DIR]:
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        dir_path.chmod(0o755)  # Ensure proper permissions
    except Exception as e:
        logger.critical(f"Failed to create directory {dir_path}: {e}")
        raise RuntimeError(f"Directory setup failed: {e}")

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# Conversion configuration
ALLOWED_FORMATS = {
    "audio": ["mp3", "wav", "ogg", "flac", "aac", "m4a"],
    "video": ["mp4", "mov", "avi", "mkv", "webm"],
}
CONVERSION_TASKS = {}


# Helper functions with improved error handling
def validate_extension(ext: str) -> bool:
    return any(ext in formats for formats in ALLOWED_FORMATS.values())


def validate_conversion(input_ext: str, output_ext: str) -> bool:
    for category in ALLOWED_FORMATS:
        if (
            input_ext in ALLOWED_FORMATS[category]
            and output_ext in ALLOWED_FORMATS[category]
        ):
            return True
    return False


async def save_upload(file: UploadFile, path: Path):
    try:
        with path.open("wb") as buffer:
            while content := await file.read(1024 * 1024):  # 1MB chunks
                buffer.write(content)
        path.chmod(0o644)  # Set proper file permissions
    except Exception as e:
        logger.error(f"File save failed: {e}")
        raise HTTPException(500, "Failed to save uploaded file")


# Routes with improved error handling
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("files.html", {"request": request})


@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...), output_format: str = Form(...)):
    if not file.filename:
        raise HTTPException(400, "No file uploaded")

    try:
        file_ext = Path(file.filename).suffix[1:].lower()
        if not validate_extension(file_ext):
            raise HTTPException(400, "Unsupported file format")

        if not validate_conversion(file_ext, output_format):
            raise HTTPException(400, "Invalid conversion type")

        task_id = str(uuid.uuid4())
        base_name = Path(file.filename).stem
        output_filename = f"{base_name}-{output_format}.{output_format}"

        # Save original file
        upload_path = UPLOAD_DIR / f"{task_id}_original.{file_ext}"
        await save_upload(file, upload_path)

        # Create conversion task
        CONVERSION_TASKS[task_id] = {
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
        logger.error(f"Unexpected error in conversion: {e}")
        raise HTTPException(500, "Internal server error")


async def process_conversion(task_id: str):
    task = CONVERSION_TASKS.get(task_id)
    if not task:
        logger.error(f"Task {task_id} not found")
        return

    try:
        task["status"] = "processing"
        logger.info(f"Starting conversion for task {task_id}")

        cmd = [
            "/usr/bin/ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(task["upload_path"]),
            str(task["output_path"]),
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=300)
        except asyncio.TimeoutError:
            logger.error(f"FFmpeg timeout for task {task_id}")
            raise RuntimeError("Conversion timed out")

        if proc.returncode != 0:
            error_msg = stderr.decode().strip()
            logger.error(f"FFmpeg failed for task {task_id}: {error_msg}")
            raise RuntimeError(f"FFmpeg error: {error_msg}")

        task["status"] = "completed"
        logger.info(f"Conversion successful for task {task_id}")

    except Exception as e:
        task["status"] = "failed"
        task["error"] = str(e)
        logger.error(f"Conversion failed for task {task_id}: {e}")
    finally:
        try:
            if task["upload_path"].exists():
                task["upload_path"].unlink()
        except Exception as e:
            logger.error(f"Cleanup error for task {task_id}: {e}")


@app.get("/api/conversion-status/{task_id}")
async def conversion_status(task_id: str):
    task = CONVERSION_TASKS.get(task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    return {
        "status": task["status"],
        "download_url": (
            f"/download/{task['output_path'].name}"
            if task["output_path"].exists()
            else None
        ),
        "error": task["error"],
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    try:
        file_path = CONVERTED_DIR / filename
        if not file_path.exists():
            raise HTTPException(404, "File not found")

        return FileResponse(
            file_path,
            media_type="application/octet-stream",
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logger.error(f"Download failed for {filename}: {e}")
        raise HTTPException(500, "File download error")


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8300))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_config=None,
        access_log=False,
    )
