from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.themes import Theme
from models.users import UserPartial, UserWithCanReceiveNotifications

__all__ = ('SecretTextMessage',)


class SecretTextMessage(BaseModel):
    id: UUID
    text: str
    sender: UserPartial
    recipient: UserWithCanReceiveNotifications
    theme: Theme | None
    deleted_at: datetime | None
    seen_at: datetime | None
    created_at: datetime

    @property
    def is_seen(self) -> bool:
        return self.seen_at is not None
