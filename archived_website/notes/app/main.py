"""
notes.dunamismax.com - A password-protected note-taking FastAPI app.

Features:
  - Single admin password (set via environment variable) for access
  - PostgreSQL database for storing, editing, and deleting notes
  - Jinja2 templates with a clean, Nord-inspired design
  - Session-based authentication using cookie middleware
"""

import logging
import os
from pathlib import Path

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

# -------------------------------------------------------------------------
# Logging & Environment Setup
# -------------------------------------------------------------------------
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("notes.log", mode="a"),
    ],
)
logger = logging.getLogger("NotesApp")

# Load environment variables (assuming .env is in the parent directory)
ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

ADMIN_PASSWORD = os.getenv("NOTES_ADMIN_PASSWORD", "changeme")
DB_HOST = os.getenv("NOTES_DB_HOST", "localhost")
DB_NAME = os.getenv("NOTES_DB_NAME", "notes_db")
DB_USER = os.getenv("NOTES_DB_USER", "notes_user")
DB_PASS = os.getenv("NOTES_DB_PASS", "notes_password")
DB_PORT = os.getenv("NOTES_DB_PORT", "5432")
SECRET_KEY = os.getenv("NOTES_SECRET_KEY", "REPLACE_WITH_SECURE_RANDOM_KEY")

# -------------------------------------------------------------------------
# FastAPI Initialization
# -------------------------------------------------------------------------
app = FastAPI(
    title="DunamisMax Notes",
    description="Password-protected note-taking application using PostgreSQL.",
    version="1.0.0",
)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


# -------------------------------------------------------------------------
# Database Helpers
# -------------------------------------------------------------------------
def get_db_connection():
    """Return a new psycopg2 connection to PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    )


def init_db():
    """Initialize the notes table if it does not exist."""
    logger.info("Initializing notes table if not exists...")
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS notes (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(create_table_sql)
        conn.commit()
    logger.info("Database initialized successfully.")


@app.on_event("startup")
async def startup_event():
    """Run on server startup."""
    logger.info("Starting up NotesApp...")
    init_db()
    logger.info("Startup complete.")


# -------------------------------------------------------------------------
# Authentication Dependency
# -------------------------------------------------------------------------
def requires_login(request: Request):
    """Dependency to ensure the user is logged in."""
    if not request.session.get("logged_in"):
        return RedirectResponse(url="/login", status_code=303)
    return True


# -------------------------------------------------------------------------
# Routes: Login & Logout
# -------------------------------------------------------------------------
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render the login page."""
    if request.session.get("logged_in"):
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def process_login(request: Request, password: str = Form(...)):
    """Process login and set session if password is correct."""
    if password == ADMIN_PASSWORD:
        request.session["logged_in"] = True
        logger.info("Admin logged in successfully.")
        return RedirectResponse(url="/", status_code=302)
    else:
        logger.warning("Failed login attempt.")
        return RedirectResponse(url="/login?error=1", status_code=302)


@app.get("/logout")
async def logout(request: Request):
    """Log out by clearing the session."""
    request.session.clear()
    logger.info("Admin logged out.")
    return RedirectResponse(url="/login", status_code=302)


# -------------------------------------------------------------------------
# Routes: Notes CRUD
# -------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def list_notes(request: Request, auth: bool = Depends(requires_login)):
    """Display all notes and a form to create a new note."""
    if isinstance(auth, RedirectResponse):
        return auth

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM notes ORDER BY created_at DESC;")
            notes = cur.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})


@app.post("/notes/create")
async def create_note(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    auth: bool = Depends(requires_login),
):
    """Insert a new note into the database."""
    if isinstance(auth, RedirectResponse):
        return auth

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO notes (title, content, updated_at) VALUES (%s, %s, NOW())",
                (title, content),
            )
        conn.commit()
    logger.info(f"Created note: {title}")
    return RedirectResponse(url="/", status_code=302)


@app.get("/notes/{note_id}/edit", response_class=HTMLResponse)
async def edit_note_form(request: Request, note_id: int, auth: bool = Depends(requires_login)):
    """Display the note editing form."""
    if isinstance(auth, RedirectResponse):
        return auth

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM notes WHERE id = %s;", (note_id,))
            note = cur.fetchone()
    if not note:
        logger.warning(f"Note ID {note_id} not found.")
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("edit_note.html", {"request": request, "note": note})


@app.post("/notes/{note_id}/edit")
async def update_note(
    request: Request,
    note_id: int,
    title: str = Form(...),
    content: str = Form(...),
    auth: bool = Depends(requires_login),
):
    """Update a note in the database."""
    if isinstance(auth, RedirectResponse):
        return auth

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE notes SET title = %s, content = %s, updated_at = NOW() WHERE id = %s",
                (title, content, note_id),
            )
        conn.commit()
    logger.info(f"Updated note ID {note_id}")
    return RedirectResponse(url="/", status_code=302)


@app.post("/notes/{note_id}/delete")
async def delete_note(request: Request, note_id: int, auth: bool = Depends(requires_login)):
    """Delete a note by its ID."""
    if isinstance(auth, RedirectResponse):
        return auth

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        conn.commit()
    logger.info(f"Deleted note ID {note_id}")
    return RedirectResponse(url="/", status_code=302)


# -------------------------------------------------------------------------
# Run the Application
# -------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    logger.info("Running DunamisMax NotesApp with Uvicorn...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("NOTES_PORT", 8500)),
        reload=os.getenv("DEBUG", "false").lower() == "true",
    )
