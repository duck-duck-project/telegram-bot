from datetime import date
from typing import NewType

from pydantic import BaseModel, HttpUrl

__all__ = ('FoodMenuItem', 'DailyFoodMenu', 'HTML')

HTML = NewType('HTML', str)


class FoodMenuItem(BaseModel):
    name: str
    calories_count: int
    photo_url: HttpUrl


class DailyFoodMenu(BaseModel):
    items: list[FoodMenuItem]
    at: date
