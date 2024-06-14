from datetime import datetime

from pydantic import BaseModel

__all__ = ('MinedResource',)


class MinedResource(BaseModel):
    user_id: int
    wealth: int
    resource_name: str
    next_mining_at: datetime
