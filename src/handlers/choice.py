import random

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters import choices_between_options_filter

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text,
    choices_between_options_filter,
    StateFilter('*'),
)
async def on_choice_between_options(
        message: Message,
        options: list[str],
) -> None:
    chosen_option = random.choice(options)
    await message.reply(f'🤔 | Я выбираю: {chosen_option}')
