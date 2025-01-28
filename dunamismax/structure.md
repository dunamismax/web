dunamismax/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── blog.py          # Blog post endpoints
│   │   ├── messenger.py     # WebSocket messenger endpoints
│   │   └── playground.py    # API demo endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── blog.py          # Blog post schemas
│   │   ├── messenger.py     # Message schemas
│   │   └── playground.py    # API playground schemas
│   ├── templates/
│   │   ├── base.html        # Base template with Nord theme
│   │   ├── partials/
│   │   │   ├── nav.html     # Navigation bar
│   │   │   ├── footer.html
│   │   │   └── messages.html # HTMX message partial
│   │   ├── pages/
│   │   │   ├── home.html
│   │   │   ├── blog.html
│   │   │   ├── messenger.html
│   │   │   ├── about.html
│   │   │   └── playground.html
│   ├── static/
│   │   ├── css/
│   │   │   ├── nord.css     # Nord theme variables
│   │   │   ├── base.css     # Global styles
│   │   │   └── components/
│   │   │       ├── nav.css
│   │   │       ├── messages.css
│   │   │       └── playground.css
│   │   └── img/            # Site images/icons
│   └── main.py            # FastAPI app initialization
├── tests/
│   ├── __init__.py
│   ├── test_blog.py
│   ├── test_messenger.py
│   └── test_playground.py
└── requirements.txt
