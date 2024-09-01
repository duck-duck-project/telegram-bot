from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import Message

__all__ = ('router',)
router = Router(name=__name__)


@router.message(
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    or_f(
        Command('timetable'),
        F.text.lower.in_({'расписание', 'timetable'}),
    ),
    F.reply_to_message.from_user.is_bot,
    StateFilter('*'),
)
async def on_show_timetable(message: Message) -> None:
    await message.reply(
        f'📆 Расписание: https://manas-timetable.vercel.app'
    )
