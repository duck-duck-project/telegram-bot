from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters import gender_filter
from repositories import UserRepository

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    gender_filter,
    StateFilter('*'),
)
async def on_gender_change(
        message: Message,
        user_repository: UserRepository,
        gender
) -> None:
    await user_repository.upsert(
        user_id=message.from_user.id,
        fullname=message.from_user.full_name,
        username=message.from_user.username,
        gender=gender,
    )
    await message.reply('✅ Вы успешно поменяли пол')


@router.message(
    F.text.lower().startswith('поменять пол'),
    StateFilter('*'),
)
async def on_gender_change_help(message: Message) -> None:
    await message.reply(
        '❓ Для смены пола, используйте команду:\n'
        '<pre>Поменять пол\n'
        '{мужской,женский,другой}</pre>'
    )
