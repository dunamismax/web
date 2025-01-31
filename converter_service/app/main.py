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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("logs/file-converter.log")],
)
logger = logging.getLogger("DunamisMaxFiles")

# Load environment variables
ENV_PATH = Path(__file__).parent.parent / ".env"
(
    load_dotenv(ENV_PATH)
    if os.path.exists(ENV_PATH)
    else logger.warning(".env file not found")
)

app = FastAPI(title=os.getenv("APP_NAME", "DunamisMax File Converter"))

# File storage paths
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
CONVERTED_DIR = BASE_DIR / "converted"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Ensure directories exist
for dir_path in [UPLOAD_DIR, CONVERTED_DIR, STATIC_DIR, TEMPLATES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)
    dir_path.chmod(0o755)

# Allowed formats with codec mappings
ALLOWED_FORMATS = {
    "audio": {
        "mp3": ["-acodec", "libmp3lame", "-ab", "192k"],
        "wav": ["-acodec", "pcm_s16le"],
        "ogg": ["-acodec", "libvorbis"],
        "flac": ["-acodec", "flac"],
        "aac": ["-acodec", "aac"],
        "m4a": ["-acodec", "aac", "-strict", "-2"],
    },
    "video": {
        "mp4": ["-vcodec", "libx264", "-acodec", "aac"],
        "mov": ["-vcodec", "libx264", "-acodec", "aac"],
        "avi": ["-vcodec", "mpeg4", "-acodec", "mp3"],
        "mkv": ["-vcodec", "libx264", "-acodec", "aac"],
        "webm": ["-vcodec", "libvpx", "-acodec", "libvorbis"],
    },
}

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

conversion_tasks = {}


async def verify_ffmpeg():
    """Verify FFmpeg installation with proper permissions"""
    try:
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        return proc.returncode == 0
    except Exception as e:
        logger.error(f"FFmpeg verification failed: {e}")
        return False


async def save_upload(file: UploadFile, path: Path):
    """Save uploaded file with chunked writing"""
    try:
        with path.open("wb") as buffer:
            while content := await file.read(16 * 1024):  # 16KB chunks
                buffer.write(content)
        path.chmod(0o644)
        return True
    except Exception as e:
        logger.error(f"File save failed: {e}")
        raise HTTPException(500, "File upload failed")


@app.get("/")
async def root(request: Request):
    """Main conversion interface"""
    return templates.TemplateResponse("files.html", {"request": request})


@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...), output_format: str = Form(...)):
    """Handle file conversion requests with improved validation"""
    if not file.filename or not output_format:
        raise HTTPException(400, "Missing required parameters")

    file_ext = Path(file.filename).suffix[1:].lower()
    output_format = output_format.lower()

    # Validate formats
    valid_formats = {fmt for fmts in ALLOWED_FORMATS.values() for fmt in fmts}
    if file_ext not in valid_formats or output_format not in valid_formats:
        raise HTTPException(400, "Unsupported file format")

    task_id = str(uuid.uuid4())
    output_filename = f"{task_id}.{output_format}"
    upload_path = UPLOAD_DIR / f"{task_id}_original.{file_ext}"
    output_path = CONVERTED_DIR / output_filename

    try:
        await save_upload(file, upload_path)

        conversion_tasks[task_id] = {
            "status": "processing",
            "output_path": output_path,
            "error": None,
        }

        asyncio.create_task(
            process_conversion(task_id, upload_path, output_path, output_format)
        )

        return {"task_id": task_id, "download_url": f"/download/{output_filename}"}

    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise HTTPException(500, "Conversion process failed")


async def process_conversion(
    task_id: str, input_path: Path, output_path: Path, fmt: str
):
    """Process conversion with proper codec handling"""
    try:
        # Determine codec parameters
        for category, formats in ALLOWED_FORMATS.items():
            if fmt in formats:
                codec_params = formats[fmt]
                break
        else:
            raise RuntimeError("Unsupported output format")

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_path),
            *codec_params,
            "-nostdin",
            "-loglevel",
            "error",
            str(output_path),
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        _, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {stderr.decode().strip()}")

        if not output_path.exists():
            raise RuntimeError("Output file not created")

        conversion_tasks[task_id]["status"] = "completed"
        logger.info(f"Successful conversion: {task_id}")

    except Exception as e:
        conversion_tasks[task_id].update({"status": "failed", "error": str(e)})
        logger.error(f"Conversion failed {task_id}: {e}")

    finally:
        # Cleanup original file
        try:
            input_path.unlink(missing_ok=True)
        except Exception as e:
            logger.error(f"Cleanup error: {e}")


@app.get("/api/conversion-status/{task_id}")
async def conversion_status(task_id: str):
    """Conversion status endpoint with improved error handling"""
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
    """Secure file download endpoint"""
    file_path = CONVERTED_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, "File not found")

    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=filename.split(".", 1)[-1],  # Original filename
    )


@app.on_event("startup")
async def startup_event():
    """Initialization with proper FFmpeg verification"""
    if not await verify_ffmpeg():
        logger.critical("FFmpeg not found - conversions will fail")
    else:
        logger.info("FFmpeg verified successfully")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8300)),
        log_level="info",
    )
