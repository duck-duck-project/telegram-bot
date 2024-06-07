from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters import create_name_filter
from repositories import UserRepository

__all__ = ('router',)

router = Router(name=__name__)

real_last_name_filter = create_name_filter(
    command_name='поменять фамилию',
    param_name='real_last_name',
)


@router.message(
    real_last_name_filter,
    StateFilter('*'),
)
async def on_real_last_name_input(
        message: Message,
        real_last_name: str,
        user_repository: UserRepository,
) -> None:
    if len(real_last_name) > 64:
        await message.reply('❌ Фамилия должна быть до 64 символов')
        return
    user, _ = await user_repository.upsert(
        user_id=message.from_user.id,
        fullname=message.from_user.full_name,
        username=message.from_user.username,
        real_last_name=real_last_name,
    )
    await message.reply(f'✅ Фамилия обновлена')


@router.message(
    F.text.startswith('поменять фамилию'),
    StateFilter('*'),
)
async def on_real_last_name_input_help(message: Message) -> None:
    await message.reply(
        '❓ Введите фамилию в формате:\n'
        '<pre>'
        'поменять фамилию\n'
        'Токтобердиев'
        '</pre>'
    )
