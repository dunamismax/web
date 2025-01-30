# Add to main.py
@app.get("/files")
async def files_page(request: Request):
    """File conversion landing page"""
    return templates.TemplateResponse("files.html", {"request": request})


@app.post("/api/convert")
async def convert_file(
    request: Request, file: UploadFile = File(...), output_format: str = Form("mp3")
):
    """Handle file conversion"""
    return await FileConverterService().handle_conversion(file, output_format)


@app.get("/api/conversion-status/{task_id}")
async def check_status(task_id: str):
    """Check conversion task status"""
    return await FileConverterService().get_status(task_id)


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download converted files"""
    return await FileConverterService().serve_file(filename)
