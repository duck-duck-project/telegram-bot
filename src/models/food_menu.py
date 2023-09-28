from typing import NewType

from pydantic import BaseModel, HttpUrl

__all__ = ('FoodMenuItem', 'HTML')

HTML = NewType('HTML', str)


class FoodMenuItem(BaseModel):
    name: str
    calories: int
    image_url: HttpUrl
