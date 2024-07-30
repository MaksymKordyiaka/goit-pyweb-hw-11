from pydantic import BaseModel
from typing import Optional
from datetime import date


class ContactBase(BaseModel):
    first_name: str
    second_name: str
    email: str
    phone: str
    birthdate: date
    additional_data: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int

    class Config:
        from_attributes = True
