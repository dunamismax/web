# DunamisMax

**DunamisMax** is a suite of modern web applications built with FastAPI. It includes a real-time Messenger and AI-powered Agents, offering seamless communication and intelligent assistance.

## Technology Stack

### Backend Framework

- **FastAPI** - Modern Python web framework for building high-performance APIs
- **Uvicorn** - Lightning-fast ASGI server implementation
- **Python 3.x** - Core programming language
- **WebSocket** - For real-time bidirectional communication
- **Jinja2** - Server-side templating engine

### Frontend

- **HTML5** - Semantic markup
- **CSS3** 
  - Custom CSS variables
  - Nord color theme
  - Flexbox and Grid layouts
  - Responsive design
- **Vanilla JavaScript** - No framework dependencies
- **Feather Icons** - SVG icon library (via CDN)
- **Fira Code** - Monospace font (via Google Fonts)

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
│   │   ├── agents.py         # AI agent logic
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
├── messenger/               # Real-time Messenger
│   ├── app/
│   │   ├── static/         # Static assets
│   │   ├── templates/      # HTML templates
│   │   ├── messenger.py   # WebSocket logic
│   │   └── main.py       # FastAPI application
│   └── requirements.txt   # Python dependencies
│
├── .gitignore             # Git ignore rules
├── LICENSE               # Project license
└── README.md            # Project documentation
```

## Features

- **Messenger:** Real-time chat using WebSockets
- **AI Agents:** Interactive AI assistants for various tasks
- **Responsive Design:** Optimized for all devices
- **Clean UI:** Consistent styling with the Nord color palette

## Key Components

- Three separate FastAPI applications:
  - **Main Site** (dunamismax.com)
  - **AI Agents** (agents.dunamismax.com)
  - **Messenger** (messenger.dunamismax.com)
- Real-time WebSocket communication
- Multi-user support
- Cross-subdomain consistent styling
- Zero-dependency frontend

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/dunamismax/DunamisMax.git
   cd DunamisMax
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   # Install dependencies for each application
   pip install -r web/dunamismax/requirements.txt
   pip install -r web/messenger/requirements.txt
   pip install -r web/ai_agents/requirements.txt
   ```

4. **Run the Applications**

   ```bash
   # Main site
   uvicorn web.dunamismax.app.main:app --host 0.0.0.0 --port 8000 --reload

   # Messenger
   uvicorn web.messenger.app.main:app --host 0.0.0.0 --port 8100 --reload

   # AI Agents
   uvicorn web.ai_agents.app.main:app --host 0.0.0.0 --port 8200 --reload
   ```

5. **Access the Applications**
   - Main Site: `http://localhost:8000`
   - Messenger: `http://localhost:8100`
   - AI Agents: `http://localhost:8200`

## Development

- Each application can be developed independently
- Uses Uvicorn's auto-reload feature for development
- Consistent styling across all applications
- Local SSL provided by Caddy

## Deployment

- Caddy handles reverse proxy and SSL
- Cloudflare manages DNS and provides CDN
- Each application runs on its own subdomain
- Automatic HTTPS certification

## Contact

- **Email:** [dunamismax@tutamail.com](mailto:dunamismax@tutamail.com)
- **GitHub:** [github.com/dunamismax](https://github.com/dunamismax)
- **Beaker Profile:** [bsky.app/profile/dunamismax.bsky.social](https://bsky.app/profile/dunamismax.bsky.social)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
