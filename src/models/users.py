from typing import Protocol

from pydantic import BaseModel, HttpUrl

from models.themes import Theme

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
    theme: Theme | None
    profile_photo_url: HttpUrl | None
    is_banned: bool
    can_receive_notifications: bool

    @property
    def username_or_fullname(self) -> str:
        return self.username or self.fullname
