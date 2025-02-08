import asyncio
import json
import logging
import os
import re
import time
import uuid
from pathlib import Path

import aiofiles
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Load environment variables
load_dotenv()

# === Parse Environment Variables ===
APP_NAME = os.getenv("APP_NAME", "DunamisMax File Converter")
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8300"))
MAX_FILE_SIZE_STR = os.getenv("MAX_FILE_SIZE", "10GB")
UPLOAD_RETENTION_HOURS = int(os.getenv("UPLOAD_RETENTION_HOURS", "24"))
CONVERSION_TIMEOUT = int(os.getenv("CONVERSION_TIMEOUT", "300"))
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
ALLOWED_FORMATS_ENV = os.getenv("ALLOWED_FORMATS", None)
MAX_CONCURRENT_CONVERSIONS = int(os.getenv("MAX_CONCURRENT_CONVERSIONS", "4"))
TEMPORARY_STORAGE = os.getenv("TEMPORARY_STORAGE", None)
ENABLE_FILE_VALIDATION = os.getenv("ENABLE_FILE_VALIDATION", "true").lower() == "true"
SANITIZE_FILENAMES = os.getenv("SANITIZE_FILENAMES", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))


def parse_size(size_str: str) -> int:
    """Parse a size string (e.g., '10GB', '100MB') into bytes."""
    size_str = size_str.strip().upper()
    if size_str.endswith("GB"):
        return int(float(size_str[:-2]) * 1024**3)
    elif size_str.endswith("MB"):
        return int(float(size_str[:-2]) * 1024**2)
    elif size_str.endswith("KB"):
        return int(float(size_str[:-2]) * 1024)
    else:
        return int(size_str)


MAX_FILE_SIZE_BYTES = parse_size(MAX_FILE_SIZE_STR)

# === Determine Directories ===
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
# If TEMPORARY_STORAGE is set, use it for processing files; otherwise, use BASE_DIR.
TEMP_DIR = Path(TEMPORARY_STORAGE) if TEMPORARY_STORAGE else BASE_DIR
UPLOAD_DIR = TEMP_DIR / "uploads"
CONVERTED_DIR = TEMP_DIR / "converted"

for directory in (LOG_DIR, UPLOAD_DIR, CONVERTED_DIR):
    directory.mkdir(parents=True, exist_ok=True)

# === Configure Logging ===
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "file-converter.log", mode="a"),
    ],
)
logger = logging.getLogger("DunamisMaxFiles")

# === Create FastAPI App ===
app = FastAPI(title=APP_NAME)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# === Allowed Formats & Codec Parameters ===
# Default codec parameters for each format:
default_audio = {
    "mp3": ["-acodec", "libmp3lame", "-ab", "192k"],
    "wav": ["-acodec", "pcm_s16le"],
    "ogg": ["-acodec", "libvorbis"],
    "flac": ["-acodec", "flac"],
    "aac": ["-acodec", "aac"],
    "m4a": ["-acodec", "aac", "-strict", "-2"],
    "wma": ["-acodec", "wmav2"],
}
default_video = {
    "mp4": ["-vcodec", "libx264", "-acodec", "aac"],
    "mov": ["-vcodec", "libx264", "-acodec", "aac"],
    "avi": ["-vcodec", "mpeg4", "-acodec", "mp3"],
    "mkv": ["-vcodec", "libx264", "-acodec", "aac"],
    "webm": ["-vcodec", "libvpx", "-acodec", "libvorbis"],
    "mpeg": ["-vcodec", "mpeg1video", "-acodec", "mp2"],
    "3gp": ["-vcodec", "h263", "-acodec", "aac"],
    "ts": ["-vcodec", "mpeg2video", "-acodec", "mp2"],
}
default_image = {
    "jpg": ["-c:v", "mjpeg"],
    "jpeg": ["-c:v", "mjpeg"],
    "png": ["-c:v", "png"],
    "gif": ["-c:v", "gif"],
    "bmp": ["-c:v", "bmp"],
    "webp": ["-c:v", "libwebp"],
    "tiff": ["-c:v", "tiff"],
    "tif": ["-c:v", "tiff"],
}

if ALLOWED_FORMATS_ENV:
    try:
        allowed_env = json.loads(ALLOWED_FORMATS_ENV)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse ALLOWED_FORMATS env variable: {e}")
        allowed_env = {}
    allowed_audio = {}
    allowed_video = {}
    if "audio" in allowed_env:
        for fmt in allowed_env["audio"]:
            if fmt in default_audio:
                allowed_audio[fmt] = default_audio[fmt]
    if "video" in allowed_env:
        for fmt in allowed_env["video"]:
            if fmt in default_video:
                allowed_video[fmt] = default_video[fmt]
    ALLOWED_FORMATS = {"audio": allowed_audio, "video": allowed_video, "image": default_image}
else:
    ALLOWED_FORMATS = {
        "audio": default_audio,
        "video": default_video,
        "image": default_image,
    }

# === Concurrency Control ===
conversion_semaphore = asyncio.Semaphore(MAX_CONCURRENT_CONVERSIONS)

# In-memory tracking of conversion tasks
conversion_tasks = {}


def sanitize_filename(filename: str) -> str:
    """Remove any unwanted characters from a filename."""
    return re.sub(r"[^A-Za-z0-9_.-]", "", filename)


# === Helper Functions ===


async def verify_ffmpeg() -> bool:
    """Verify that FFmpeg is installed and accessible."""
    try:
        proc = await asyncio.create_subprocess_exec(
            FFMPEG_PATH,
            "-version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        return proc.returncode == 0
    except Exception as e:
        logger.error(f"FFmpeg verification failed: {e}")
        return False


async def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """
    Save an uploaded file to disk in chunks to avoid memory issues.
    """
    try:
        async with aiofiles.open(destination, "wb") as out_file:
            while True:
                chunk = await upload_file.read(1024 * 1024)  # 1MB chunks
                if not chunk:
                    break
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Failed to save uploaded file: {e}")
        raise
    finally:
        await upload_file.close()


# === Routes ===


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("files.html", {"request": request})


@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...), output_format: str = Form(...)):
    try:
        logger.info(f"Received conversion request: {file.filename} -> {output_format}")
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        original_filename = file.filename
        if SANITIZE_FILENAMES:
            original_filename = sanitize_filename(original_filename)

        file_ext = Path(original_filename).suffix[1:].lower()
        output_format = output_format.lower()

        # Build a set of valid formats from ALLOWED_FORMATS
        valid_formats = {fmt for category in ALLOWED_FORMATS.values() for fmt in category.keys()}
        if file_ext not in valid_formats or output_format not in valid_formats:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {output_format}")

        if ENABLE_FILE_VALIDATION:
            # Validate file size by seeking to the end of the underlying file
            try:
                file.file.seek(0, 2)
                size = file.file.tell()
                file.file.seek(0)
                if size > MAX_FILE_SIZE_BYTES:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File too large. Maximum allowed is {MAX_FILE_SIZE_STR}.",
                    )
            except Exception as e:
                logger.error(f"Failed to validate file size: {e}")

        task_id = str(uuid.uuid4())
        upload_path = UPLOAD_DIR / f"{task_id}_original.{file_ext}"
        output_path = CONVERTED_DIR / f"{task_id}.{output_format}"

        # Save the uploaded file in chunks
        await save_upload_file(file, upload_path)

        # Track the conversion task and kick off processing asynchronously
        conversion_tasks[task_id] = {
            "status": "processing",
            "output_path": output_path,
            "error": None,
        }
        asyncio.create_task(process_conversion(task_id, upload_path, output_path, output_format))

        return {
            "task_id": task_id,
            "status": "processing",
            "download_url": f"/download/{output_path.name}",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Conversion request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


async def process_conversion(
    task_id: str, input_path: Path, output_path: Path, output_format: str
) -> None:
    """
    Run the FFmpeg conversion process asynchronously with concurrency and timeout controls.
    """
    try:
        # Find codec parameters for the desired output format.
        codec_params = None
        for formats in ALLOWED_FORMATS.values():
            if output_format in formats:
                codec_params = formats[output_format]
                break
        if not codec_params:
            raise ValueError(f"No codec parameters for format: {output_format}")

        ffmpeg_cmd = [
            FFMPEG_PATH,
            "-y",
            "-i",
            str(input_path),
            *codec_params,
            str(output_path),
        ]
        logger.info(f"Starting FFmpeg with command: {' '.join(ffmpeg_cmd)}")

        # Limit the number of concurrent conversions
        async with conversion_semaphore:
            proc = await asyncio.create_subprocess_exec(
                *ffmpeg_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(), timeout=CONVERSION_TIMEOUT
                )
            except asyncio.TimeoutError:
                proc.kill()
                raise RuntimeError("Conversion timed out")

            if proc.returncode != 0:
                error_message = stderr.decode().strip()
                raise RuntimeError(f"FFmpeg error: {error_message}")

        conversion_tasks[task_id]["status"] = "completed"
        logger.info(f"Conversion task {task_id} completed successfully.")
    except Exception as e:
        logger.exception(f"Conversion failed for task {task_id}: {e}")
        conversion_tasks[task_id].update({"status": "failed", "error": str(e)})
    finally:
        try:
            input_path.unlink(missing_ok=True)
        except Exception as e:
            logger.error(f"Failed to remove temporary file {input_path}: {e}")


@app.get("/api/conversion-status/{task_id}")
async def get_conversion_status(task_id: str):
    task = conversion_tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "status": task["status"],
        "error": task["error"],
        "download_url": f"/download/{task['output_path'].name}"
        if task["status"] == "completed"
        else None,
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = CONVERTED_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)


@app.get("/privacy")
async def privacy(request: Request):
    try:
        logger.info("Rendering privacy page")
        return templates.TemplateResponse(
            "privacy.html", {"request": request, "page_title": "Privacy Policy - DunamisMax"}
        )
    except Exception as e:
        logger.exception(f"Error rendering privacy page: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# === Background Cleanup Task ===
async def cleanup_old_files():
    """
    Periodically delete files from the upload and conversion directories that are older than the retention period.
    """
    while True:
        now = time.time()
        cutoff = now - (UPLOAD_RETENTION_HOURS * 3600)
        for directory in [UPLOAD_DIR, CONVERTED_DIR]:
            for file in directory.iterdir():
                if file.is_file() and file.stat().st_mtime < cutoff:
                    try:
                        file.unlink()
                        logger.info(f"Cleaned up old file: {file}")
                    except Exception as e:
                        logger.error(f"Error cleaning up file {file}: {e}")
        await asyncio.sleep(3600)  # Run cleanup every hour


@app.on_event("startup")
async def startup_event():
    if not await verify_ffmpeg():
        logger.critical("FFmpeg not found or not working")
    else:
        logger.info("FFmpeg verified successfully.")
    logger.info("File Converter service started")
    # Start the background cleanup task
    asyncio.create_task(cleanup_old_files())


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
    )
