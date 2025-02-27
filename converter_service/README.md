# DunamisMax File Converter

High-performance file conversion service built with FastAPI. Part of the DunamisMax suite of web applications. Supports various audio and video formats with real-time conversion progress tracking.

## Features

- **Real-time conversion progress tracking**
- **Multiple format support** for audio and video files
- **Drag-and-drop file uploads** for convenience
- **Streaming upload and download** support
- **Secure and efficient processing** using FFmpeg
- **Error handling and automatic cleanup**
- **Modern, user-friendly web interface**
- **Logging for monitoring and debugging**

## Technology Stack

### Backend

- **FastAPI** - Web framework
- **FFmpeg** - Media processing
- **Uvicorn** - ASGI server
- **Python 3.x** - Core language
- **asyncio** - Asynchronous processing

### Frontend

- **HTML5** - Markup structure
- **CSS3** - Styling and responsiveness
- **JavaScript** - Interactive elements
- **Jinja2** - Templating engine
- **Feather Icons** - UI icons
- **Fira Code** - Monospace font

### Infrastructure

- **Caddy** - Reverse proxy
- **Cloudflare** - DNS and CDN
- **FFmpeg** - Media processing

## Project Structure

```bash
converter_service/
├── app/
│   ├── static/
│   │   ├── favicon.ico      # Site favicon
│   │   ├── logo.svg         # Site logo
│   │   └── styles.css       # Stylesheet
│   ├── templates/
│   │   ├── base.html        # Base template
│   │   ├── files.html       # File upload/conversion page
│   │   └── privacy.html     # Privacy policy page
│   ├── uploads/             # Uploaded files
│   ├── converted/           # Converted files
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── converter_service.py # File conversion logic
├── logs/
│   ├── file-converter.log   # Log file for monitoring
├── .env                     # Environment variables
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
```

## Supported Formats

### Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- OGG (.ogg)
- FLAC (.flac)
- AAC (.aac)
- M4A (.m4a)

### Video Formats

- MP4 (.mp4)
- MOV (.mov)
- AVI (.avi)
- MKV (.mkv)
- WebM (.webm)

## Installation

1. **Install FFmpeg**

   ```bash
   sudo nala update
   sudo apt install ffmpeg
   ```

2. **Set Up Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   ```bash
   cp .env.example .env
   # Edit .env with necessary API keys and settings
   ```

5. **Run the Application**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8300 --reload
   ```

6. **Access the Service**
   - Local: `http://localhost:8300`
   - Production: `https://files.dunamismax.com`

## API Endpoints

### File Operations

- `POST /api/convert` - Convert uploaded file
- `GET /api/conversion-status/{task_id}` - Check conversion status
- `GET /download/{filename}` - Download converted file

### Status Responses

```javascript
{
    "status": "queued|processing|completed|failed",
    "download_url": "string|null",
    "error": "string|null"
}
```

## Logging & Debugging

- Logs are stored in `logs/file-converter.log`
- Use `tail -f logs/file-converter.log` to monitor activity

## Security Features

- Environment variable configuration
- Input validation for uploaded files
- Rate limiting via Cloudflare
- Secure file handling and auto-cleanup
- File size and format restrictions

## Deployment

- Runs on port 8300
- Reverse proxy managed via Caddy
- Cloudflare CDN and DNS setup
- Automatic SSL/TLS enforcement

## Contributing

1. Fork the repository
2. Create a feature branch:

   ```bash
   git checkout -b feature/new-feature
   ```

3. Commit changes:

   ```bash
   git commit -m "Add new feature"
   ```

4. Push to GitHub:

   ```bash
   git push origin feature/new-feature
   ```

5. Create a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
