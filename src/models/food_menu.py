from datetime import date
from typing import NewType

from pydantic import BaseModel, HttpUrl

from enums import FoodItemType

__all__ = ('FoodItem', 'FoodMenuItem', 'DailyFoodMenu', 'HTML')

HTML = NewType('HTML', str)


class FoodItem(BaseModel):
    name: str
    energy_benefit_value: int
    emoji: str | None
    price: int
    type: FoodItemType
    health_impact_value: int


class FoodMenuItem(BaseModel):
    name: str
    calories_count: int
    photo_url: HttpUrl


class DailyFoodMenu(BaseModel):
    items: list[FoodMenuItem]
    at: date
