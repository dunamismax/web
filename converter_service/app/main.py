from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn

# Import the FileConverterService
from app.converter_service import FileConverterService

# ✅ Define FastAPI app
app = FastAPI(title="DunamisMax File Converter")

# ✅ Mount static files
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)

# ✅ Set up Jinja templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


# ✅ Add the missing ROOT ("/") route
@app.get("/")
async def root(request: Request):
    """Redirect root to the files page"""
    return templates.TemplateResponse("files.html", {"request": request})


# ✅ Route: File conversion landing page
@app.get("/files")
async def files_page(request: Request):
    return templates.TemplateResponse("files.html", {"request": request})


# ✅ Route: Handle file conversion
@app.post("/api/convert")
async def convert_file(file: UploadFile = File(...)):
    return await FileConverterService().handle_conversion(file)


# ✅ Route: Check conversion task status
@app.get("/api/conversion-status/{task_id}")
async def check_status(task_id: str):
    return await FileConverterService().get_status(task_id)


# ✅ Route: Download converted file
@app.get("/download/{filename}")
async def download_file(filename: str):
    return await FileConverterService().serve_file(filename)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8300, reload=True)
