import traceback
from collections.abc import Iterable

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message

from middlewares.common import Handler, ContextData

__all__ = ('MirrorMiddleware',)


class MirrorMiddleware(BaseMiddleware):

    def __init__(self, mirror_chat_id: int, ignored_chat_ids: Iterable[int]):
        self.__mirror_chat_id = mirror_chat_id
        self.__ignored_chat_ids = set(ignored_chat_ids)

    async def __call__(
            self,
            handler: Handler,
            event: Message,
            data: ContextData,
    ) -> None:
        if event.chat.id not in self.__ignored_chat_ids:
            try:
                await event.forward(chat_id=self.__mirror_chat_id)
            except TelegramAPIError:
                traceback.print_exc()

        return await handler(event, data)
