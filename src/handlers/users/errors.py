from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import UserDoesNotExistError

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(UserDoesNotExistError))
async def on_user_does_not_exist_error(event: ErrorEvent) -> None:
    update = event.update
    text = '😔 Данный пользователь не существует'
    if update.message is not None:
        await update.message.reply(text)
    if update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
