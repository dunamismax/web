# FastAPI Chatbot Application

A robust CLI chatbot application built with FastAPI and OpenAI's API, featuring multiple AI personas and real-time chat capabilities.

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8203 --reload
```

## Features

- Multiple AI personas with different expertise and personalities
- Real-time chat interface with command-line UI
- Rate limiting and request throttling
- Comprehensive logging system
- Type-safe configuration management
- CORS support
- Error handling and validation
- Thread-safe implementation

## Prerequisites

- Python 3.8+
- OpenAI API key
- Poetry (recommended) or pip for dependency management

## Project Structure

```bash
└── 📁chatbot
    └── 📁app
        ├── __init__.py
        ├── config.py        # Configuration management
        ├── logger.py        # Logging setup
        ├── main.py         # FastAPI application
        ├── rate_limiter.py # Rate limiting logic
        └── chat_service.py # Chat service implementation
    └── 📁client
        └── client.py       # CLI client implementation
    ├── .env               # Environment variables
    ├── README.md
    └── requirements.txt
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/chatbot.git
cd chatbot
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your configuration:

```env
OPENAI_API_KEY=your_api_key_here
DEBUG=False
HOST=0.0.0.0
PORT=8203
MAX_WEBSOCKET_CONNECTIONS=1000
RATE_LIMIT_PER_MINUTE=10
LOG_LEVEL=INFO
MODEL_NAME=gpt-3.5-turbo
```

## Usage

### Starting the Server

1. Start the FastAPI server:

```bash
python -m app.main
```

The server will start at `http://localhost:8203` by default.

### Running the CLI Client

1. In a separate terminal, run the client:

```bash
python client/client.py
```

2. Select a chatbot persona from the available options.

3. Start chatting! Use the following commands:

- `/quit` or `/exit` - Exit the application
- `/back` - Return to chatbot selection

## API Endpoints

### Health Check

```http
GET /
```

Returns the API status.

### Chat Endpoint

```http
POST /chat
```

Send messages to the chatbot.

#### Request Body

```json
{
    "message": "Your message here",
    "prompt": "System prompt for the AI"
}
```

#### Response

```json
{
    "role": "assistant",
    "content": "AI response here"
}
```

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| OPENAI_API_KEY | Your OpenAI API key | Required |
| DEBUG | Enable debug mode | False |
| HOST | Server host | 0.0.0.0 |
| PORT | Server port | 8203 |
| MAX_WEBSOCKET_CONNECTIONS | Maximum concurrent connections | 1000 |
| RATE_LIMIT_PER_MINUTE | Request rate limit per client | 10 |
| LOG_LEVEL | Logging level | INFO |
| MODEL_NAME | OpenAI model to use | gpt-3.5-turbo |

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
isort .
```

## Error Handling

The application includes comprehensive error handling:

- Rate limiting errors (429)
- Input validation errors (400)
- Server errors (500)
- API errors with detailed messages

## Logging

Logs are written to both console and `app.log` file, including:

- Request/response details
- Error tracing
- Performance metrics
- Rate limiting events

## Security Considerations

- API key protection
- Rate limiting per client
- Input validation
- CORS configuration (customize for production)
- Thread-safe implementations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for their ChatGPT API
- FastAPI framework
- Python Prompt Toolkit for the CLI interface
- Nord color theme for the terminal UI

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
