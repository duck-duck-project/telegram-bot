from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from repositories import RelationshipRepository
from views import (
    RelationshipBreakUpConfirmationView,
    RelationshipBreakUpResultView,
    answer_view,
    reply_view,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower() == 'да, я уверен и хочу расстаться',
    StateFilter('*'),
)
async def on_break_up(
        message: Message,
        relationship_repository: RelationshipRepository
) -> None:
    break_up_result = await relationship_repository.break_up(
        user_id=message.from_user.id,
    )
    view = RelationshipBreakUpResultView(break_up_result)
    await answer_view(message=message, view=view)


@router.message(
    F.text.lower() == 'расстаться',
    StateFilter('*')
)
async def on_show_break_up_confirmation(message: Message) -> None:
    view = RelationshipBreakUpConfirmationView()
    await reply_view(message=message, view=view)
