# DunamisMax AI Agents

Interactive AI chat interface built with FastAPI, WebSockets, and chatgpt-4o-latest. Part of the DunamisMax suite of web applications.

## Features

- Real-time AI chat interactions
- Multiple specialized AI agents
- Streaming responses for immediate feedback
- Intelligent problem-solving
- Natural conversation flow
- Chat history within session
- Responsive design for all devices
- Connection status indicators
- Error handling and recovery
- Automatic reconnection
- Clean Nord-themed interface

## Technology Stack

### Backend

- FastAPI - Web framework
- WebSockets - Real-time communication
- Uvicorn - ASGI server
- Python 3.x - Core language
- chatgpt-4o-latest - AI language model

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
ai_agents/
├── app/
│   ├── static/
│   │   ├── favicon.ico     # Site favicon
│   │   ├── logo.svg        # Site logo
│   │   └── styles.css      # Stylesheets
│   ├── templates/
│   │   ├── base.html       # Base template
│   │   ├── chat.html       # Chat interface
│   │   └── index.html      # Agent selection
│   ├── __init__.py
│   ├── agents.py          # AI agent definitions
│   └── main.py           # FastAPI application
├── .env                  # Environment variables
├── README.md
└── requirements.txt
```

## Available Agents

Each agent is specialized for specific tasks:

1. **General Assistant**
   - Task assistance
   - Information queries
   - General guidance
   - Problem-solving

2. **Code Assistant**
   - Programming help
   - Code review
   - Debugging assistance
   - Technical guidance

3. **Research Assistant**
   - Information gathering
   - Topic exploration
   - Data analysis
   - Knowledge synthesis

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

3. **Configure Environment Variables**

   ```bash
   cp .env.example .env
   # Edit .env with your OPENAI_API_KEY and other settings
   ```

4. **Run the Application**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8200 --reload
   ```

5. **Access the Application**
   - Local development: `http://localhost:8200`
   - Production: `https://agents.dunamismax.com`

## WebSocket Protocol

### Message Format

```javascript
{
    "type": "message|system|error",
    "role": "user|assistant",
    "content": "Message content",
    "agent_id": "agent-identifier",
    "is_chunk": boolean,
    "is_complete": boolean
}
```

### Streaming Responses

- Real-time response streaming
- Final chunk marked with `is_complete: true`
- Error handling for incomplete streams

## Development

### Adding New Agents

1. Define agent in `agents.py`:

   ```python
   class NewAgent(BaseAgent):
       id = "unique-id"
       name = "Agent Name"
       description = "Agent capabilities"
       icon = "feather-icon-name"
   ```

2. Register in available agents:

   ```python
   available_agents = {
       "new-agent": NewAgent()
   }
   ```

### Testing

```bash
# Run tests
python -m pytest tests/
```

## Error Handling

- Connection state management
- Automatic reconnection logic
- Rate limiting protection
- Input validation
- Response validation
- System notifications for errors

## Security Features

- Environment variable configuration
- Input sanitization
- Rate limiting (via Cloudflare)
- Secure WebSocket connections
- Error message sanitization
- API key protection

## Deployment

- Runs on port 8200
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
