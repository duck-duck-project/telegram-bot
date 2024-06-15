from datetime import datetime

from pydantic import BaseModel

__all__ = ('MinedResource', 'MinedResourceStatistics', 'MiningUserStatistics')


class MinedResource(BaseModel):
    user_id: int
    wealth: int
    resource_name: str
    next_mining_at: datetime


class MinedResourceStatistics(BaseModel):
    name: str
    total_wealth: int
    total_count: int


class MiningUserStatistics(BaseModel):
    user_id: int
    resources: list[MinedResourceStatistics]
