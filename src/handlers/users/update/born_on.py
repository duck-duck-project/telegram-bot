from datetime import date

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters import birth_date_filter
from repositories import UserRepository

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text,
    birth_date_filter,
    StateFilter('*'),
)
async def on_update_birth_date(
        message: Message,
        birth_date: date,
        user_repository: UserRepository,
) -> None:
    user, _ = await user_repository.upsert(
        user_id=message.from_user.id,
        fullname=message.from_user.full_name,
        username=message.from_user.username,
        born_on=birth_date,
    )
    await message.reply('Your birth date has been updated.')
