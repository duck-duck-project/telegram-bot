from uuid import UUID

from pydantic import BaseModel

from models.users import User

__all__ = ('SecretMessage',)


class SecretMessage(BaseModel):
    id: UUID
    text: str
    sender: User
    recipient: User
    is_seen: bool
    is_deleted: bool
    created_at: str
