from aiogram import F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.types import Message

from filters import role_play_trigger_filter
from models import RolePlayAction
from views import RolePlayActionView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text,
    F.reply_to_message,
    F.reply_to_message.from_user.id != F.from_user.id,
    invert_f(F.reply_to_message.from_user.is_bot),
    role_play_trigger_filter,
    StateFilter('*'),
)
async def on_role_play_action(
        message: Message,
        role_play_action: RolePlayAction,
) -> None:
    view = RolePlayActionView(
        role_play_action=role_play_action,
        message=message,
    )
    await answer_view(message=message, view=view)
