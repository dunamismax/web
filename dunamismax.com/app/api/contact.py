from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

from ..db.database import execute
from ..db.queries import INSERT_CONTACT
from ..models.contact_model import ContactModel

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/contact", include_in_schema=False, response_class=HTMLResponse)
@logger.catch
async def submit_contact(
    request: Request, form_data: ContactModel = Depends(ContactModel)
):
    """
    Receives contact form data (via HTMX) and saves it into the DB.
    Returns an HTML snippet on success, replacing the form.
    """
    pool = request.app.state.pool
    await execute(
        pool, INSERT_CONTACT, form_data.name, form_data.email, form_data.message
    )

    # Return a partial template snippet, confirming success
    return templates.TemplateResponse(
        "partials/contact_success.html", {"request": request, "name": form_data.name}
    )
