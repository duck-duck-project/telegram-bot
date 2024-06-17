from pydantic import BaseModel

__all__ = (
    'MinedResourceResult',
    'MinedResourceStatistics',
    'MiningUserStatistics',
)


class MinedResourceResult(BaseModel):
    user_id: int
    resource_name: str
    value: int
    value_per_gram: int | float
    weight_in_grams: int
    spent_energy: int
    remaining_energy: int


class MinedResourceStatistics(BaseModel):
    name: str
    total_value: int
    total_count: int


class MiningUserStatistics(BaseModel):
    user_id: int
    resources: list[MinedResourceStatistics]
