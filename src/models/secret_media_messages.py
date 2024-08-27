from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from enums import SecretMediaType
from models.themes import Theme
from models.users import UserPartial

__all__ = ('SecretMediaMessage',)


class SecretMediaMessage(BaseModel):
    id: UUID
    file_id: str
    media_type: SecretMediaType
    caption: str | None
    sender: UserPartial
    recipient: UserPartial
    theme: Theme | None
    created_at: datetime
