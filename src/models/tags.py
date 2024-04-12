from datetime import datetime

from pydantic import BaseModel

from enums import TagWeight

__all__ = ('Tag',)


class Tag(BaseModel):
    id: int
    text: str
    weight: TagWeight
    created_at: datetime
    of_user_fullname: str
    of_user_username: str | None
