from aiogram.filters import Filter
from aiogram.types import Message

__all__ = ('PhotoDimensionsFilter',)


class PhotoDimensionsFilter(Filter):

    def __init__(self, *, max_ratio: int | float):
        self.__max_ratio = max_ratio

    async def __call__(self, message: Message) -> bool | dict:
        photo = message.photo[-1]
        ratio = abs(
            max(photo.width, photo.height) /
            min(photo.width, photo.height)
        )
        return ratio <= self.__max_ratio
