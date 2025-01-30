from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
import logging
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ✅ Define FastAPI app
app = FastAPI(title="DunamisMax File Converter")

# ✅ Resolve absolute paths for directories
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
CONVERTED_DIR = BASE_DIR / "converted"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# ✅ Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CONVERTED_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# ✅ Mount static files using absolute path
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
else:
    logger.error(f"❌ Static directory '{STATIC_DIR}' does not exist!")

# ✅ Set up Jinja templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ✅ Import and instantiate the FileConverterService
from app.converter_service import FileConverterService

converter_service = FileConverterService()


# ✅ Route: Serve file conversion page
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("files.html", {"request": request})


# ✅ Route: Handle file conversion
@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...), output_format: str = Form(...)):
    """Receives a file and starts conversion."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    logger.info(f"📥 Received file: {file.filename} -> {output_format}")
    return await converter_service.handle_conversion(file, output_format)


# ✅ Route: Check conversion task status
@app.get("/api/conversion-status/{task_id}")
async def check_status(task_id: str):
    """Checks the status of an ongoing file conversion."""
    return await converter_service.get_status(task_id)


# ✅ Route: Download converted file
@app.get("/download/{filename}")
async def download_file(filename: str):
    """Serves converted files for download."""
    converted_path = CONVERTED_DIR / filename
    upload_path = UPLOAD_DIR / filename

    if converted_path.exists():
        return await converter_service.serve_file(filename)
    elif upload_path.exists():
        return await converter_service.serve_file(filename, from_upload=True)

    raise HTTPException(404, "File not found.")


# ✅ Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8300, reload=True)
