from datetime import datetime

from pydantic import BaseModel

from enums import TagWeight
from models.users import UserPartial

__all__ = ('UserTag', 'UserTags', 'Tag')


class Tag(BaseModel):
    id: int
    text: str
    weight: TagWeight
    created_at: datetime
    of_user_fullname: str
    of_user_username: str | None


class UserTag(BaseModel):
    id: int
    of_user: UserPartial
    text: str
    weight: TagWeight
    created_at: datetime


class UserTags(BaseModel):
    user: UserPartial
    tags: tuple[UserTag, ...]
