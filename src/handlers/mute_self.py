import time

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.types import ChatPermissions, Message

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower() == 'помолчать',
    StateFilter('*'),
)
async def on_mute_self(message: Message, bot: Bot):
    until_date = int(time.time()) + 3600 * 2
    is_restricted = await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        permissions=ChatPermissions(
            can_send_messages=False,
        ),
        until_date=until_date,
    )
    if is_restricted:
        await message.answer(
            f'🔇 {message.from_user.mention_html()} решил помолчать на 2 часа',
        )
