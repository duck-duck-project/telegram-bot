from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters import create_name_filter
from repositories import UserRepository

__all__ = ('router',)

router = Router(name=__name__)

real_first_name_filter = create_name_filter(
    command_name='поменять имя',
    param_name='real_first_name',
)


@router.message(
    real_first_name_filter,
    StateFilter('*'),
)
async def on_real_first_name_input(
        message: Message,
        real_first_name: str,
        user_repository: UserRepository,
) -> None:
    if len(real_first_name) > 64:
        await message.reply('❌ Имя должно быть до 64 символов')
        return
    user, _ = await user_repository.upsert(
        user_id=message.from_user.id,
        fullname=message.from_user.full_name,
        username=message.from_user.username,
        real_first_name=real_first_name,
    )
    await message.reply('✅ Имя обновлено')


@router.message(
    F.text.lower().startswith('поменять имя'),
    StateFilter('*'),
)
async def on_real_first_name_input_help(message: Message) -> None:
    await message.reply(
        '❓ Введите имя в формате:\n'
        '<pre>'
        'поменять имя\n'
        'Адилет'
        '</pre>'
    )
