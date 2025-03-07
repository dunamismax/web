# DunamisMax Technology Stack

## Backend Framework

- **FastAPI** - Modern Python web framework for building high-performance APIs
- **Uvicorn** - Lightning-fast ASGI server implementation
- **Python 3.x** - Core programming language
- **WebSocket** - For real-time bidirectional communication
- **Jinja2** - Server-side templating engine

## Frontend

- **HTML5** - Semantic markup
- **CSS3**
  - Custom CSS variables
  - Nord color theme
  - Flexbox and Grid layouts
  - Responsive design
- **Vanilla JavaScript** - No framework dependencies
- **Feather Icons** - SVG icon library (via CDN)
- **Fira Code** - Monospace font (via Google Fonts)

## Infrastructure & Deployment

- **Caddy** - Modern reverse proxy server
  - Automatic HTTPS
  - Zero-config SSL
  - HTTP/3 support
- **Cloudflare**
  - DNS management
  - CDN services
  - DDoS protection
  - SSL/TLS encryption

## Application Architecture

Three separate FastAPI applications:

- **Main Site** (dunamismax.com)
- **AI Agents** (agents.dunamismax.com)
- **Messenger** (messenger.dunamismax.com)

## Key Features

- Real-time WebSocket communication
- Stateful connection management
- Multi-user support
- Responsive design
- Cross-subdomain consistent styling
- Zero-dependency frontend
- Modern HTTP/2 and HTTP/3 support

## Development Environment

- Version Control: Git
- Development Server: Uvicorn with auto-reload
- Local SSL: Caddy automatic HTTPS

## Notable Characteristics

- Minimalist dependency approach
- High performance
- Modern security practices
- Developer-friendly setup
- Easy deployment pipeline
