from typing import Protocol

from pydantic import BaseModel, HttpUrl

from models.themes import SecretMessageTheme

__all__ = ('HasUserId', 'User', 'UserPartial')


class HasUserId(Protocol):
    user_id: int


class UserPartial(BaseModel):
    id: int
    username: str | None
    fullname: str


class User(BaseModel):
    id: int
    fullname: str
    username: str | None
    can_be_added_to_contacts: bool
    secret_message_theme: SecretMessageTheme | None
    profile_photo_url: HttpUrl | None
    is_banned: bool
    can_receive_notifications: bool
