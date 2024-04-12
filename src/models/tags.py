from datetime import datetime

from pydantic import BaseModel

from enums import TagWeight

__all__ = ('Tag',)


class Tag(BaseModel):
    id: int
    text: str
    weight: TagWeight
    created_at: datetime
