import os
import uuid
import logging
import asyncio
import aiofiles  # Added this import
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
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/file-converter.log", mode="a"),
    ],
)
logger = logging.getLogger("DunamisMaxFiles")

# Load environment variables
load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "DunamisMax File Converter"))

# File storage paths
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
CONVERTED_DIR = BASE_DIR / "converted"

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CONVERTED_DIR.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Track conversion tasks
conversion_tasks = {}

# Get allowed formats from environment
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


async def verify_ffmpeg():
    """Verify FFmpeg installation"""
    try:
        proc = await asyncio.create_subprocess_exec(
            os.getenv("FFMPEG_PATH", "ffmpeg"),
            "-version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        return proc.returncode == 0
    except Exception as e:
        logger.error(f"FFmpeg verification failed: {e}")
        return False


@app.get("/")
async def root(request: Request):
    """Render the main page"""
    return templates.TemplateResponse("files.html", {"request": request})


@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...), output_format: str = Form(...)):
    """Handle file conversion requests"""
    try:
        # Log the incoming request
        logger.info(
            f"Received conversion request for file: {file.filename} to {output_format}"
        )

        # Validate file and format
        if not file.filename:
            logger.warning("No file provided in request")
            raise HTTPException(400, "No file provided")

        file_ext = Path(file.filename).suffix[1:].lower()
        output_format = output_format.lower()

        # Log format information
        logger.info(f"File extension: {file_ext}, Target format: {output_format}")

        # Check if formats are supported
        valid_formats = {fmt for fmts in ALLOWED_FORMATS.values() for fmt in fmts}
        if file_ext not in valid_formats or output_format not in valid_formats:
            logger.warning(f"Unsupported format requested: {output_format}")
            raise HTTPException(400, f"Unsupported format: {output_format}")

        # Generate unique ID and paths
        task_id = str(uuid.uuid4())
        upload_path = UPLOAD_DIR / f"{task_id}_original.{file_ext}"
        output_path = CONVERTED_DIR / f"{task_id}.{output_format}"

        logger.info(f"Created task {task_id}")
        logger.info(f"Upload path: {upload_path}")
        logger.info(f"Output path: {output_path}")

        # Save uploaded file with error handling
        try:
            content = await file.read()
            async with aiofiles.open(str(upload_path), "wb") as buffer:
                await buffer.write(content)
            logger.info(f"Successfully saved uploaded file to {upload_path}")
        except Exception as e:
            logger.error(f"Failed to save uploaded file: {e}")
            raise HTTPException(500, f"Failed to save uploaded file: {str(e)}")

        # Initialize conversion task
        conversion_tasks[task_id] = {
            "status": "processing",
            "output_path": output_path,
            "error": None,
        }

        # Start conversion process
        asyncio.create_task(
            process_conversion(task_id, upload_path, output_path, output_format)
        )

        logger.info(f"Conversion task {task_id} initialized successfully")
        return {
            "task_id": task_id,
            "status": "processing",
            "download_url": f"/download/{output_path.name}",
        }

    except Exception as e:
        logger.error(f"Conversion request failed: {str(e)}", exc_info=True)
        # Cleanup any partial files
        if "upload_path" in locals():
            try:
                upload_path.unlink(missing_ok=True)
            except Exception as cleanup_error:
                logger.error(f"Cleanup failed: {cleanup_error}")

        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(500, f"Internal server error: {str(e)}")


async def process_conversion(
    task_id: str, input_path: Path, output_path: Path, output_format: str
):
    """Process the actual conversion"""
    try:
        # Get codec parameters
        codec_params = None
        for category, formats in ALLOWED_FORMATS.items():
            if output_format in formats:
                codec_params = formats[output_format]
                break

        if not codec_params:
            raise ValueError(f"No codec parameters for format: {output_format}")

        # Build FFmpeg command
        cmd = [
            os.getenv("FFMPEG_PATH", "ffmpeg"),
            "-y",
            "-i",
            str(input_path),
            *codec_params,
            str(output_path),
        ]

        # Run conversion
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {stderr.decode()}")

        conversion_tasks[task_id]["status"] = "completed"
        logger.info(f"Conversion task {task_id} completed successfully")

    except Exception as e:
        logger.error(f"Conversion failed for task {task_id}: {e}")
        conversion_tasks[task_id].update({"status": "failed", "error": str(e)})
    finally:
        # Cleanup input file
        try:
            input_path.unlink(missing_ok=True)
        except Exception as e:
            logger.error(f"Cleanup failed for {input_path}: {e}")


@app.get("/api/conversion-status/{task_id}")
async def get_conversion_status(task_id: str):
    """Get the status of a conversion task"""
    task = conversion_tasks.get(task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    return {
        "status": task["status"],
        "error": task["error"],
        "download_url": (
            f"/download/{task['output_path'].name}"
            if task["status"] == "completed"
            else None
        ),
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Handle file downloads"""
    file_path = CONVERTED_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, "File not found")

    return FileResponse(
        file_path, media_type="application/octet-stream", filename=filename
    )


@app.get("/privacy")
async def privacy(request: Request):
    """Render the privacy policy page"""
    try:
        logger.info("Rendering privacy page")
        return templates.TemplateResponse(
            "privacy.html",
            {
                "request": request,
                "page_title": "Privacy Policy - DunamisMax",
            },
        )
    except Exception as e:
        logger.error(f"Error rendering privacy page: {e}", exc_info=True)
        raise


@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    if not await verify_ffmpeg():
        logger.critical("FFmpeg not found or not working")
    logger.info("File Converter service started")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8300)),
        reload=os.getenv("DEBUG", "false").lower() == "true",
    )
