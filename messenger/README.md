# DunamisMax Messenger

Real-time messaging application built with FastAPI and WebSockets. Part of the DunamisMax suite of web applications.

## Features

- Real-time bidirectional communication using WebSockets
- Clean, minimal interface with Nord theme
- Username-based chat rooms
- System notifications for user join/leave events
- Responsive design for all devices
- Connection status indicators
- Message persistence during session
- Automatic reconnection on disconnection

## Technology Stack

### Backend

- FastAPI - Web framework
- WebSockets - Real-time communication
- Uvicorn - ASGI server
- Python 3.x - Core language

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
- WebSocket secure connections (wss://)

## Project Structure

```bash
messenger/
├── app/
│   ├── static/
│   │   ├── favicon.ico      # Site favicon
│   │   ├── logo.svg         # Site logo
│   │   └── styles.css       # Stylesheets
│   ├── templates/
│   │   ├── base.html        # Base template
│   │   └── index.html       # Main messenger interface
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   └── messenger.py        # WebSocket logic
├── README.md
└── requirements.txt
```

## Installation

1. **Set Up Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8100 --reload
   ```

4. **Access the Application**
   - Local development: `http://localhost:8100`
   - Production: `https://messenger.dunamismax.com`

## WebSocket Events

### Client Events

- `connect` - Initial connection with username
- `disconnect` - User leaves chat
- `message` - New message sent

### Server Events

- `system` - System notifications (user join/leave)
- `message` - Broadcast messages to all users
- `error` - Error notifications

## Message Format

```javascript
{
    "type": "message|system",
    "username": "user123",
    "text": "Message content",
    "timestamp": "2025-01-30T12:34:56.789Z"
}
```

## Development

- Uses Uvicorn's auto-reload feature for development
- WebSocket connections handled by FastAPI
- Styling matches DunamisMax main theme
- Real-time message broadcasting

## Error Handling

- Username collision detection
- Connection state management
- Automatic reconnection attempts
- Graceful error messages
- Connection status indicators

## Security Features

- HTML escape for message content
- Username validation and sanitization
- Secure WebSocket connections (wss://)
- Rate limiting (via Cloudflare)

## Deployment

- Runs on port 8100
- Reverse proxied through Caddy
- SSL/TLS provided by Cloudflare
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
