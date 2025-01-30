from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
import logging
import os

# ✅ Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Define FastAPI app
app = FastAPI(title="DunamisMax File Converter")

# ✅ Ensure Upload and Converted directories exist
UPLOAD_DIR = Path("/home/sawyer/github/web/converter_service/uploads")
CONVERTED_DIR = Path("/home/sawyer/github/web/converter_service/converted")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CONVERTED_DIR.mkdir(parents=True, exist_ok=True)

# ✅ Mount static files
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)

# ✅ Set up Jinja templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# ✅ Import the FileConverterService (after directory check)
from app.converter_service import FileConverterService


# ✅ Route: Root ("/") serves files.html
@app.get("/")
async def root(request: Request):
    """Serve file conversion page"""
    return templates.TemplateResponse("files.html", {"request": request})


# ✅ Route: Handle file conversion
@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...)):
    """Handles file upload and starts conversion process"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    logger.info(f"Received file: {file.filename}")

    return await FileConverterService().handle_conversion(file)


# ✅ Route: Check conversion task status
@app.get("/api/conversion-status/{task_id}")
async def check_status(task_id: str):
    """Checks the status of an ongoing file conversion"""
    return await FileConverterService().get_status(task_id)


# ✅ Route: Download converted file
@app.get("/download/{filename}")
async def download_file(filename: str):
    """Serves converted files for download"""
    return await FileConverterService().serve_file(filename)


# ✅ Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8300, reload=True)
