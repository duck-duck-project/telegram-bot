from datetime import date, datetime

from pydantic import BaseModel

from models.themes import Theme
from models.users import UserPartial, UserWithProfilePhotoUrl, UserWithTheme

__all__ = ('Contact', 'ContactBirthday', 'UserContacts', 'UserContact')


class Contact(BaseModel):
    id: int
    user: UserWithProfilePhotoUrl
    private_name: str
    public_name: str
    is_hidden: bool
    theme: Theme | None
    created_at: datetime


class UserContacts(BaseModel):
    user: UserWithTheme
    contacts: list[Contact]


class UserContact(BaseModel):
    user: UserWithTheme
    contact: Contact


class ContactBirthday(BaseModel):
    user: UserPartial
    born_on: date
