from datetime import date, datetime
from typing import Protocol

from pydantic import BaseModel, HttpUrl

from enums import ContactsSortingStrategy, Gender
from models.themes import Theme

__all__ = (
    'HasUserId',
    'User',
    'UserPartial',
    'UserEnergyRefill',
    'UserSportsActivityResult',
)


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
    is_blocked_bot: bool
    personality_type: str | None
    born_on: date | None
    real_first_name: str | None
    real_last_name: str | None
    patronymic: str | None
    gender: Gender | None
    nationality: str | None
    region: str | None
    country: str | None
    country_flag_emoji: str | None
    contacts_sorting_strategy: ContactsSortingStrategy
    is_contacts_sorting_reversed: bool
    energy: int
    health: int
    did_sports_at: datetime | None

    @property
    def username_or_fullname(self) -> str:
        return self.username or self.fullname


class UserEnergyRefill(BaseModel):
    user_id: int
    energy: int


class UserSportsActivityResult(BaseModel):
    user_id: int
    health: int
