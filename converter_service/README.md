# DunamisMax File Converter

High-performance file conversion service built with FastAPI. Part of the DunamisMax suite of web applications. Supports various audio and video formats with real-time conversion progress tracking.

## Features

- Real-time conversion progress
- Multiple format support
- Audio format conversion
- Video format conversion
- Streaming upload/download
- Progress indicators
- Error handling and recovery
- Automatic cleanup
- Clean Nord-themed interface
- Drag-and-drop file uploads

## Technology Stack

### Backend

- FastAPI - Web framework
- FFmpeg - Media conversion
- Uvicorn - ASGI server
- Python 3.x - Core language
- asyncio - Asynchronous I/O

### Frontend

- HTML5 - Semantic markup
- CSS3 - Styling
  - CSS Variables
  - Nord color theme
  - Flexbox/Grid layouts
- Vanilla JavaScript - No framework dependencies
- Feather Icons - UI icons
- Fira Code - Monospace font

### Infrastructure

- Caddy - Reverse proxy
- Cloudflare - DNS and CDN
- FFmpeg - Media processing

## Project Structure

```bash
converter_service/
├── app/
│   ├── static/
│   │   ├── favicon.ico      # Site favicon
│   │   ├── logo.svg         # Site logo
│   │   └── styles.css       # Stylesheets
│   ├── templates/
│   │   ├── base.html        # Base template
│   │   └── files.html       # File upload interface
│   ├── uploads/             # Temporary upload storage
│   ├── converted/           # Converted file storage
│   ├── __init__.py
│   └── main.py             # FastAPI application
├── logs/                   # Application logs
├── .env                    # Environment variables
├── README.md
└── requirements.txt
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
   sudo apt update
   sudo apt install ffmpeg
   ```

2. **Set Up Virtual Environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the Application**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8300 --reload
   ```

6. **Access the Application**
   - Local development: `http://localhost:8300`
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

## Development

### Environment Variables

```env
APP_NAME="DunamisMax File Converter"
ENVIRONMENT="production"
DEBUG=false
HOST="0.0.0.0"
PORT=8300
MAX_FILE_SIZE="100MB"
FFMPEG_PATH="/usr/bin/ffmpeg"
```

### Testing

```bash
# Run tests
python -m pytest tests/
```

## Error Handling

- File size validation
- Format validation
- Conversion monitoring
- Cleanup on failure
- Input sanitization
- Progress tracking
- System notifications

## Security Features

- File type validation
- Size restrictions
- Input sanitization
- Rate limiting
- File cleanup
- Safe file naming

## Deployment

- Runs on port 8300
- Reverse proxied through Caddy
- SSL/TLS via Cloudflare
- Automatic HTTPS redirection

## Contributing

1. Fork the repository
2. Create your feature branch

   ```bash
   git checkout -b feature/new-feature
   ```

3. Commit your changes

   ```bash
   git commit -am 'Add new feature'
   ```

4. Push to the branch

   ```bash
   git push origin feature/new-feature
   ```

5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
