from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import SecretMessageDoesNotExistError

__all__ = ('register_handlers',)


async def on_secret_message_does_not_exist_error(event: ErrorEvent) -> None:
    await event.update.callback_query.answer(
        'Сообщение не найдено. Возможно оно ещё не загружено на наши сервера.'
        ' Попробуйте через пару секунд',
        show_alert=True,
    )


def register_handlers(router: Router) -> None:
    router.errors.register(
        on_secret_message_does_not_exist_error,
        ExceptionTypeFilter(SecretMessageDoesNotExistError),
    )
