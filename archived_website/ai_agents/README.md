# DunamisMax AI Agents

High-performance AI chat service built with FastAPI, WebSockets, and ChatGPT-4o. Part of the DunamisMax suite of web applications, offering real-time, interactive AI experiences with multiple specialized agents.

## Features

- **Real-time AI chat interactions** with streaming responses
- **Multiple specialized AI agents** tailored for different tasks
- **WebSocket-based communication** for seamless updates
- **Session-based chat history**
- **User-friendly and responsive web interface**
- **Error handling and automatic reconnection**
- **Secure and efficient processing**
- **Logging for monitoring and debugging**

## Technology Stack

### Backend

- **FastAPI** - Web framework
- **WebSockets** - Real-time communication
- **Uvicorn** - ASGI server
- **Python 3.x** - Core language
- **ChatGPT-4o** - AI language model
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
- **Secure WebSocket (wss://) connections**

## Project Structure

```bash
dunamismax_ai_agents/
├── app/
│   ├── static/
│   │   ├── favicon.ico      # Site favicon
│   │   ├── logo.svg         # Site logo
│   │   └── styles.css       # Stylesheet
│   ├── templates/
│   │   ├── base.html        # Base template
│   │   ├── chat.html        # Chat interface
│   │   └── index.html       # Agent selection
│   ├── __init__.py
│   ├── agents.py            # AI agent definitions
│   └── main.py              # FastAPI application entry point
├── logs/
│   ├── ai-agents.log        # Log file for monitoring
├── .env                     # Environment variables
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
```

## Available AI Agents

### 1. System Administrator

- IT infrastructure and server management
- Troubleshooting and security guidance

### 2. Hacker

- Ethical hacking and cybersecurity advice
- Penetration testing methodologies

### 3. IT Support

- Technical assistance and troubleshooting
- Common software/hardware issue resolution

### 4. Python Developer

- Python programming guidance
- Code debugging and best practices

### 5. Linus Torvalds

- Insights into Linux and open-source development
- Kernel programming discussions

### 6. Bible Scholar

- Scriptural interpretation and historical context
- Religious discussions and theological analysis

### 7. Statistician

- Data analysis and statistical modeling
- Probability and quantitative research

### 8. Research Scientist

- Scientific methodology and research guidance
- Experiment design and data interpretation

### 9. Chess Grandmaster

- Chess strategy and tactics
- Game analysis and training techniques

### 10. Business Consultant

- Business strategy and market analysis
- Financial and operational planning

### 11. Lawyer

- Legal consultation and case evaluation
- Contract law, intellectual property, and compliance

### 12. University Professor

- Academic guidance and mentoring
- Teaching strategies and curriculum design

### 13. Psychologist

- Cognitive and behavioral insights
- Mental health advice and counseling techniques

### 14. History Professor

- Historical analysis and interpretations
- Researching historical events and figures

### 15. Writer

- Creative writing tips and storytelling guidance
- Editing and content structuring

### 16. Digital Artist

- Digital painting and graphic design techniques
- Software and creative workflow advice

### 17. Music Teacher

- Music theory and instrument instruction
- Composition and performance guidance

### 18. Fitness Coach

- Workout routines and exercise science
- Nutrition and health coaching

### 19. Chef

- Cooking techniques and recipe suggestions
- Culinary tips for various cuisines

### 20. Mechanic

- Vehicle diagnostics and repair guidance
- Auto maintenance tips and troubleshooting

### 21. Translator

- Multilingual translation and language learning
- Linguistic structure and cultural insights

### 22. Gardener

- Plant care and landscaping advice
- Sustainable gardening techniques

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
   # Edit .env with necessary API keys and settings
   ```

4. **Run the Application**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8200 --reload
   ```

5. **Access the Application**
   - Local: `http://localhost:8200`
   - Production: `https://agents.dunamismax.com`

## WebSocket Communication

### Message Format

```json
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

- Responses are streamed in real-time
- The final chunk is marked with `is_complete: true`
- Errors are handled gracefully with automatic reconnection

## Logging & Debugging

- Logs are stored in `logs/ai-agents.log`
- Use `tail -f logs/ai-agents.log` to monitor activity

## Security Features

- **Environment variable configuration** for API keys
- **Input validation** for preventing malformed data
- **Rate limiting via Cloudflare**
- **Secure WebSocket connections** with TLS encryption
- **Automatic error handling and sanitization**

## Deployment

- Runs on port 8200
- Reverse proxy managed via Caddy
- Cloudflare for CDN and DNS
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
