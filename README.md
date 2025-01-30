# DunamisMax

**DunamisMax** is a professional suite of modern web applications built with FastAPI and powered by o1-mini AI reasoning. It offers seamless real-time communication and intelligent assistance through its integrated services.

## Core Services

### [Main Site](https://dunamismax.com)

Central hub for accessing all DunamisMax services and information.

- Service directory
- Documentation access
- Project overview

### [Messenger](https://messenger.dunamismax.com)

Real-time communication platform using WebSocket technology.

- Instant messaging
- User presence indicators
- Session persistence
- Automatic reconnection

### [AI Agents](https://agents.dunamismax.com)

Suite of specialized AI assistants powered by o1-mini with advanced reasoning capabilities.

- Multiple reasoning-enhanced agents
- Step-by-step problem decomposition
- Chain-of-thought processing
- Real-time response streaming
- Context-aware conversations
- Interactive chat interface

## Technology Stack

### Backend Framework

- **FastAPI** - Modern Python web framework for building high-performance APIs
- **o1-mini** - AI language model with reasoning capabilities
- **Uvicorn** - Lightning-fast ASGI server implementation
- **Python 3.x** - Core programming language
- **WebSocket** - For real-time bidirectional communication
- **Jinja2** - Server-side templating engine
- **Custom Reasoning Engine** - Advanced logical processing system

### AI & Reasoning Stack

- **o1-mini** - Core AI model
- **Chain-of-thought Engine** - Step-by-step reasoning
- **Context Manager** - Maintains conversation context
- **Pattern Recognition** - Identifies solution patterns
- **Logic Validator** - Ensures reasoning consistency

### Frontend

- **HTML5** - Semantic markup
- **CSS3**
  - Custom CSS variables
  - Nord color theme
  - Flexbox/Grid layouts
  - Responsive design
- **Vanilla JavaScript** - No framework dependencies
- **Feather Icons** - SVG icon library
- **Fira Code** - Monospace font

### Infrastructure & Deployment

- **Caddy** - Modern reverse proxy server
  - Automatic HTTPS
  - Zero-config SSL
  - HTTP/3 support
- **Cloudflare**
  - DNS management
  - CDN services
  - DDoS protection
  - SSL/TLS encryption

## Project Structure

```bash
web/
├── ai_agents/                  # AI Agents Application
│   ├── app/
│   │   ├── static/            # Static assets
│   │   ├── templates/         # HTML templates
│   │   ├── agents.py         # AI agent definitions
│   │   ├── reasoning.py      # Reasoning engine
│   │   └── main.py          # FastAPI application
│   ├── .env                 # Environment variables
│   └── requirements.txt     # Python dependencies
│
├── dunamismax/               # Main Website
│   ├── app/
│   │   ├── static/          # Static assets
│   │   ├── templates/       # HTML templates
│   │   └── main.py         # FastAPI application
│   └── requirements.txt    # Python dependencies
│
└── messenger/               # Real-time Messenger
    ├── app/
    │   ├── static/         # Static assets
    │   │   ├── templates/  # HTML templates
    │   │   ├── messenger.py# WebSocket logic
    │   │   └── main.py    # FastAPI application
    └── requirements.txt   # Python dependencies
```

## Quick Start

1. **Clone the Repository**

   ```bash
   git clone https://github.com/dunamismax/DunamisMax.git
   cd DunamisMax
   ```

2. **Set Up Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   # Install for each service
   pip install -r web/dunamismax/requirements.txt
   pip install -r web/messenger/requirements.txt
   pip install -r web/ai_agents/requirements.txt
   ```

4. **Configure AI Environment**

   ```bash
   # Set up AI agents environment
   cp web/ai_agents/.env.example web/ai_agents/.env
   # Add your O1_API_KEY and configure reasoning settings
   ```

5. **Launch Services**

   ```bash
   # Main site (Port 8000)
   uvicorn web.dunamismax.app.main:app --host 0.0.0.0 --port 8000 --reload

   # Messenger (Port 8100)
   uvicorn web.messenger.app.main:app --host 0.0.0.0 --port 8100 --reload

   # AI Agents (Port 8200)
   uvicorn web.ai_agents.app.main:app --host 0.0.0.0 --port 8200 --reload
   ```

## Development Setup

### Prerequisites

- Python 3.11+
- o1-mini API access
- Git

### Environment Configuration

- Configure o1-mini API key in ai_agents/.env
- Set up reasoning engine parameters
- Configure environment variables as needed
- See individual service READMEs for specific settings

### Local Development

1. Start services in development mode (see Launch Services above)
2. Access development endpoints:
   - Main: <http://localhost:8000>
   - Messenger: <http://localhost:8100>
   - AI Agents: <http://localhost:8200>

## Production Deployment

### Infrastructure Requirements

- Linux server with Python 3.11+
- Caddy server installed and configured
- Cloudflare account for DNS management
- Valid o1-mini API key

### Deployment Steps

1. Clone repository to production server
2. Set up Python virtual environments
3. Configure o1-mini credentials
4. Install production dependencies
5. Configure Caddy reverse proxy
6. Set up Cloudflare DNS and SSL
7. Launch services using production settings

## Service Documentation

- [AI Agents Documentation](/ai_agents/README.md)
- [Messenger Documentation](/messenger/README.md)
- [Main Site Documentation](/dunamismax/README.md)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -am 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact & Support

- **Email:** [dunamismax@tutamail.com](mailto:dunamismax@tutamail.com)
- **GitHub:** [github.com/dunamismax](https://github.com/dunamismax)
- **Bluesky:** [bsky.app/profile/dunamismax.bsky.social](https://bsky.app/profile/dunamismax.bsky.social)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

© 2024 DunamisMax. All rights reserved.
