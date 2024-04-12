from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import TagDoesNotBelongToUserError, TagDoesNotExistError

__all__ = ('on_tag_does_not_exist_error',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(TagDoesNotBelongToUserError))
async def on_tag_does_not_belong_to_user_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        await event.update.message.reply('❌ Награда не принадлежит вам')
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(
            text='❌ Награда не принадлежит вам',
            show_alert=True,
        )


@router.error(ExceptionTypeFilter(TagDoesNotExistError))
async def on_tag_does_not_exist_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        await event.update.message.reply('❌ Награда не найдена')
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(
            text='❌ Награда не найдена',
            show_alert=True,
        )
