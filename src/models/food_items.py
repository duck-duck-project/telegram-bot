from pydantic import BaseModel

from enums import FoodItemType

__all__ = ('FoodItem',)


class FoodItem(BaseModel):
    name: str
    emoji: str | None
    type: FoodItemType
    price: int
    energy_benefit_value: int
    health_impact_value: int
