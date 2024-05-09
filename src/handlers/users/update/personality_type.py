from aiogram import F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.types import Message

from enums import PersonalityTypePrefix, PersonalityTypeSuffix
from filters import personality_type_filter
from repositories import UserRepository

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower().startswith('тип личности'),
    invert_f(personality_type_filter),
    StateFilter('*'),
)
async def on_invalid_personality_type_input(message: Message) -> None:
    await message.reply(
        '❌ Неверный формат.'
        '\n'
        'Подробнее можно почитать тут:'
        ' https://eldos.notion.site/2f36cf83627e47eb843efa93c12c121b',
    )


@router.message(
    F.text,
    personality_type_filter,
    StateFilter('*'),
)
async def on_personality_type_input(
        message: Message,
        user_repository: UserRepository,
        personality_type_prefix: PersonalityTypePrefix,
        personality_type_suffix: PersonalityTypeSuffix,
) -> None:
    user, _ = await user_repository.upsert(
        user_id=message.from_user.id,
        fullname=message.from_user.full_name,
        username=message.from_user.username,
        personality_type_prefix=personality_type_prefix,
        personality_type_suffix=personality_type_suffix,
    )
    await message.reply('✅ Тип личности обновлен')
