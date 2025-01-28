# **Core Stack**  

1. **Backend**  
   - **Python**: Vanilla implementations with native async/await. No abstraction layers.  
   - **FastAPI**: Async-first endpoints using Starlette core. Automatic OpenAPI docs with OAuth2 security schemas.  
   - **Pydantic v2**: Strict validation through `Field()` constraints and imperative validators.  
   - **Uvicorn**: ASGI deployment with WebSocket support.  

2. **Frontend**  
   - **HTMX (CDN)**: Hypermedia-driven interactions without JavaScript. Use `hx-*` attributes for all dynamic behavior.  
   - **Jinja2**: Server-rendered HTML fragments for HTMX responses. No client-side templating.  
   - **Plain CSS**: Vanilla stylesheets with CSS variables. No frameworks or preprocessors.  

3. **Database**  
   - **PostgreSQL**: Complex queries written in raw SQL.  
   - **SQLAlchemy Core + asyncpg**: Async connection pooling. No ORM - direct SQL execution.  

4. **Tooling**  
   - **HTTPX**: Async HTTP client for testing FastAPI endpoints and external service calls.  
   - **Loguru**: Zero-boilerplate structured logging with async support.  
   - **Ruff/Black**: Aggressive linting and uncompromising code formatting.  
   - **Single `requirements.txt`**: Unified dependencies with hashed constraints.
