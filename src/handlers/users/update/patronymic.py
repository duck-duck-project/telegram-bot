from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters import create_name_filter
from repositories import UserRepository

__all__ = ('router',)

router = Router(name=__name__)

patronymic_filter = create_name_filter(
    command_name='поменять отчество',
    param_name='patronymic',
)


@router.message(
    patronymic_filter,
    StateFilter('*'),
)
async def on_patronymic_input(
        message: Message,
        patronymic: str,
        user_repository: UserRepository,
) -> None:
    if len(patronymic) > 64:
        await message.reply('❌ Отчество должно быть до 64 символов')
        return
    user, _ = await user_repository.upsert(
        user_id=message.from_user.id,
        fullname=message.from_user.full_name,
        username=message.from_user.username,
        patronymic=patronymic,
    )
    await message.reply('✅ Отчество обновлено')


@router.message(
    F.text.startswith('поменять отчество'),
    StateFilter('*'),
)
async def on_patronymic_input_help(message: Message) -> None:
    await message.reply(
        '❓ Введите отчество в формате:\n'
        '<pre>'
        'поменять отчество\n'
        'Токтобердиевич'
        '</pre>'
    )
