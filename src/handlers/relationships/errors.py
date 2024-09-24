from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import (
    UserHasActiveRelationshipError,
    UserHasNoRelationshipError,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(UserHasNoRelationshipError))
async def on_user_has_no_relationship_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        await event.update.message.reply('😔 У вас нет отношений')
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(
            text='😔 У вас нет отношений',
            show_alert=True,
        )


@router.error(ExceptionTypeFilter(UserHasActiveRelationshipError))
async def on_user_has_active_relationship_error(event: ErrorEvent) -> None:
    if event.update.message is not None:
        await event.update.message.reply('😔 У кого-то уже есть отношения')
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(
            text='😔 У кого-то уже есть отношения',
            show_alert=True,
        )
