from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.users import UserPartial

__all__ = ('Transfer',)


class Transfer(BaseModel):
    id: UUID
    sender: UserPartial
    recipient: UserPartial
    amount: int
    description: str | None
    created_at: datetime

    class Config:
        use_enum_values = True
