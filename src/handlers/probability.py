import random

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from services import get_random_emoji

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower().startswith('вероятность того что'),
    StateFilter('*'),
)
async def on_ask_for_probability(message: Message):
    text = (
        f'<i>❓ {message.text}</i>\n'
        f'{get_random_emoji()} <b>{random.randint(0, 100)}%</b>'
    )
    await message.reply(text)
