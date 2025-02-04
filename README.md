# DunamisMax

**DunamisMax** is a professional suite of modern web applications built with Python & FastAPI, leveraging powerful AI integrations. Each application runs independently, providing specialized functionality such as real-time chat, AI assistants, file conversion, and note-taking—all unified by consistent design and deployment principles.

## Live Demos

- [🌐 Main Site](https://dunamismax.com) - Gateway portal for all DunamisMax services
- [💬 Messenger](https://messenger.dunamismax.com) - Real-time communication platform
- [🤖 AI Agents](https://agents.dunamismax.com) - Suite of specialized AI assistants
- [📁 File Converter](https://files.dunamismax.com) - Multi-format file conversion service
- [📝 Notes](https://notes.dunamismax.com/login) - Secure note-taking system

## Architecture

DunamisMax consists of multiple FastAPI projects, each providing a specialized service:

```bash
web/
├── ai_agents/          # AI assistant services
├── converter_service/  # File conversion functionality
├── dunamismax/        # Main site and gateway
├── messenger/         # Real-time chat platform
├── notes/            # Note-taking system
└── shared/           # Common utilities and configurations
```

Each service maintains its own independent structure with dedicated:

- FastAPI application code (`app/`)
- Templates (`templates/`)
- Static assets (`static/`)
- Dependencies (`requirements.txt`)

## Technology Stack

### Backend Infrastructure

- **FastAPI** - High-performance Python web framework
- **Python 3.x** - Core programming language
- **OpenAI GPT-4** - Advanced language model integration
- **WebSocket** - Real-time bidirectional communication
- **Uvicorn** - ASGI server implementation

### Frontend Components

- **HTML5/CSS3** - Responsive design with Nord theme
- **Vanilla JavaScript** - Minimal dependency client-side logic
- **Feather Icons** - Consistent SVG icon system
- **Fira Code** - Modern monospace typography

### DevOps & Infrastructure

- **Caddy** - Modern reverse proxy with automatic HTTPS
- **Cloudflare** - DNS, CDN, and security services
- **systemd** - Service management and auto-restart capability

## Getting Started

### Local Development Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/dunamismax/web.git
   cd web
   ```

2. **Create Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Service Dependencies**

   ```bash
   # Install dependencies for each service
   for service in ai_agents converter_service dunamismax messenger notes; do
       cd $service
       pip install -r requirements.txt
       cd ..
   done
   ```

4. **Configure Environment**
   - Copy `.env.example` to `.env` in each service directory
   - Add required credentials and configuration
   - Key variables include:
     - `OPENAI_API_KEY` (for AI Agents)
     - `DATABASE_URL`
     - `SECRET_KEY`

5. **Launch Services**

   ```bash
   # Example: Start the main site
   cd dunamismax
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Production Deployment

1. **System Requirements**
   - Python 3.8+
   - systemd (Linux)
   - Caddy or Nginx
   - SSL certificates (via Cloudflare or Let's Encrypt)

2. **Deployment Steps**

   ```bash
   # Clone repository
   git clone https://github.com/dunamismax/web.git
   cd web

   # Set up virtual environment
   python3 -m venv /opt/dunamismax/venv
   source /opt/dunamismax/venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Configure systemd services
   sudo cp deployment/systemd/* /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now dunamismax.service
   ```

3. **Reverse Proxy Configuration**

   ```caddy
   # Caddyfile example
   dunamismax.com {
       reverse_proxy localhost:8000
       tls {
           dns cloudflare
       }
   }
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 conventions
- Use type hints for function parameters
- Document all public functions and classes
- Maintain consistent error handling patterns

### Testing

- Write unit tests for core functionality
- Use pytest for test automation
- Maintain >80% code coverage
- Run tests before committing changes

### Git Workflow

1. Create feature branch (`feature/new-feature`)
2. Make focused, atomic commits
3. Write clear commit messages
4. Submit pull request for review
5. Address review feedback
6. Merge after approval

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
5. Ensure CI tests pass
6. Wait for review and approval

## Support & Contact

- **Email**: [dunamismax@tutamail.com](mailto:dunamismax@tutamail.com)
- **GitHub**: [github.com/dunamismax](https://github.com/dunamismax)
- **Bluesky**: [@dunamismax.bsky.social](https://bsky.app/profile/dunamismax.bsky.social)

## License

This project is licensed under the MIT License. © 2025 DunamisMax. All rights reserved.

See [LICENSE](LICENSE) for the full text.
