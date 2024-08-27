from json import JSONDecodeError

from aiogram import Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Update

__all__ = ('register_global_error_handlers',)


async def on_json_decode_error(event: Update) -> None:
    if event.message is not None:
        await event.message.reply(
            text='Не получилось декодировать данные с сервера',
        )
    if event.callback_query is not None:
        await event.callback_query.answer(
            text='Не получилось декодировать данные с сервера',
            show_alert=True,
        )


def register_global_error_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.error.register(
        on_json_decode_error,
        ExceptionTypeFilter(JSONDecodeError),
    )