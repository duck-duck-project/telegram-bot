from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import ContactDoesNotExistError, ContactAlreadyExistsError

__all__ = ('router',)

router = Router(name=__name__)


@router.error(
    ExceptionTypeFilter(ContactDoesNotExistError),
)
async def on_contact_does_not_exist_error(event: ErrorEvent) -> None:
    text = '😔 Контакт не существует или был удален'
    if event.update.message is not None:
        await event.update.message.answer(text)
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(text, show_alert=True)


@router.error(
    ExceptionTypeFilter(ContactAlreadyExistsError),
)
async def on_contact_already_exists_error(event: ErrorEvent) -> None:
    text = '😶 Этот пользователь уже есть в ваших контактах'
    if event.update.message is not None:
        await event.update.message.answer(text)
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(text, show_alert=True)
