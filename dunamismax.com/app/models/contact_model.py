from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    """
    Basic model for the contact form data.
    """

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    message: str = Field(min_length=1, max_length=1000)
