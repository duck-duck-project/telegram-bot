from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import ThemeDoesNotExistError

__all__ = ('register_handlers',)


async def on_theme_does_not_exist_error(event: ErrorEvent) -> None:
    await event.update.message.reply('Тема не найдена')


def register_handlers(router: Router) -> None:
    router.errors.register(
        on_theme_does_not_exist_error,
        ExceptionTypeFilter(ThemeDoesNotExistError),
    )
