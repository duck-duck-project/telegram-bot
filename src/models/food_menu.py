from datetime import date
from typing import NewType

from pydantic import BaseModel, HttpUrl

from enums import FoodType

__all__ = ('FoodItem', 'FoodMenuItem', 'DailyFoodMenu', 'HTML')

HTML = NewType('HTML', str)


class FoodItem(BaseModel):
    name: str
    energy: int
    emoji: str
    price: int
    type: FoodType


class FoodMenuItem(BaseModel):
    name: str
    calories_count: int
    photo_url: HttpUrl


class DailyFoodMenu(BaseModel):
    items: list[FoodMenuItem]
    at: date
