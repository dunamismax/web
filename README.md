# DunamisMax

**DunamisMax** is a **professional suite of modern web applications** built with **Python & FastAPI**, leveraging powerful AI integrations (e.g., **chatgpt-4o-latest**). Each app runs independently, providing specialized functionality such as **real-time chat**, **AI assistants**, **file conversion**, and **note-taking**—all unified by consistent design and deployment principles.

---

## Overview

DunamisMax comprises **multiple FastAPI projects**, each located in a subfolder under `web/`.
These services can be launched independently or together, providing a cohesive ecosystem:

- **Main Site** (`dunamismax/`) – Gateway portal for all DunamisMax services and information.
- **Messenger** (`messenger/`) – Real-time communication platform with WebSocket technology.
- **AI Agents** (`ai_agents/`) – Suite of specialized AI assistants (chat-based, context-aware).
- **File Converter** (`converter_service/`) – Powerful, multi-format file conversion service.
- **Notes** (`notes/`) – Simple note-taking system with secure login and CRUD functionality.

A high-level glimpse (not exhaustive) of the repo layout:

```bash
web/
├── ai_agents/
├── converter_service/
├── dunamismax/
├── messenger/
├── notes/
└── ...
```

**Note**: Each folder contains its own `app/` directory with FastAPI code, `templates/`, `static/`, and a `requirements.txt`.

---

## Core Technologies

### Backend

- **FastAPI** – High-performance Python framework for APIs & web services
- **Python 3.x** – Core language
- **OpenAI GPT** – Advanced AI language model usage (where applicable)
- **WebSocket** – Real-time bidirectional communication (Messenger app)
- **Uvicorn** – ASGI server for running FastAPI apps

### Frontend

- **HTML5 / CSS3** – Responsive design with custom CSS variables and Nord color theme
- **Vanilla JavaScript** – Lightweight interactivity with minimal dependencies
- **Feather Icons** – SVG icon library for consistent visual identity
- **Fira Code** – Monospace font for modern appearance

### Infrastructure

- **Caddy** – Reverse proxy with auto-HTTPS, HTTP/3, easy SSL
- **Cloudflare** – DNS management, CDN, DDoS protection
- **Docker / systemd** (optional) – Some apps may use containerization or systemd services

---

## Quick Start

1. **Clone the Repository**

   ```bash
   git clone https://github.com/dunamismax/web.git
   cd web
   ```

2. **Set Up a Python Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies** (per service)

   ```bash
   cd ai_agents
   pip install -r requirements.txt

   cd ../converter_service
   pip install -r requirements.txt

   # Repeat for dunamismax, messenger, notes if needed
   ```

4. **Configure Environment Variables**
   - Each service has a `.env` file with environment-specific settings (e.g., `OPENAI_API_KEY` for AI Agents).
   - Copy any sample `.env.example` if provided, then add your credentials.

5. **Run a Service Locally**

   ```bash
   # Example: Run the main site (dunamismax) on port 8000
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Access the Service**
   - [http://localhost:8000](http://localhost:8000) for the main site
   - Messenger, AI Agents, File Converter, or Notes similarly (using their respective ports).

---

## Development Workflow

1. **Edit Code** in the relevant subfolder under `web/`.
2. **Live Reload** with `uvicorn ... --reload` during development.
3. **Logs** often stored in each subfolder’s `logs/` directory.
4. **Testing** may involve local or container-based setups; see individual README files in each service folder.

---

## Production Deployment

1. **Clone** the repo on a production server.
2. **Install** Python dependencies in a virtual environment.
3. **Configure** environment variables (`.env` files) with production settings.
4. **Use** a reverse proxy (Caddy or Nginx) + SSL via Cloudflare or other providers.
5. **Run** each FastAPI app as a system service or Docker container for stability.

> **Tip**: Check `LICENSE`, `tech_stack.md`, and `port_structure.md` in the root for specific guidelines on licensing, port assignments, and deployment notes.

---

## Contributing

We welcome pull requests, feature suggestions, and bug reports. Please:

1. **Fork** the repository.
2. **Create** a feature branch (`git checkout -b feature/some-new-feature`).
3. **Commit** your changes (`git commit -m 'Added some new feature'`).
4. **Push** to your branch (`git push origin feature/some-new-feature`).
5. **Open** a Pull Request on GitHub.

---

## Contact & Support

- **Email**: [dunamismax@tutamail.com](mailto:dunamismax@tutamail.com)
- **GitHub**: [github.com/dunamismax](https://github.com/dunamismax)
- **Bluesky**: [bsky.app/profile/dunamismax.bsky.social](https://bsky.app/profile/dunamismax.bsky.social)

---

## License

This project is licensed under the [MIT License](LICENSE). © 2025 DunamisMax. All rights reserved.
