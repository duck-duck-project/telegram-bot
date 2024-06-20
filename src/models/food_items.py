from pydantic import BaseModel

from enums import FoodItemType

__all__ = ('FoodItem', 'FoodItemConsumptionResult')


class FoodItem(BaseModel):
    name: str
    emoji: str | None
    type: FoodItemType
    price: int
    energy_benefit_value: int
    health_impact_value: int


class FoodItemConsumptionResult(BaseModel):
    user_id: int
    food_item_name: str
    food_item_emoji: str | None
    price: int
    energy_benefit_value: int
    health_impact_value: int
    user_health: int
    user_energy: int
