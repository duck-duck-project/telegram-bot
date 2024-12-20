import random

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

__all__ = ('router',)

router = Router(name=__name__)


def to_snake_case(text: str) -> str:
    whitespace = ' '
    while whitespace * 2 in text:
        text = text.replace(whitespace * 2, whitespace)
    return text.lower().replace(whitespace, '_')


@router.message(
    F.text.lower().in_({'bool', 'бул', 'забуллить'}),
    F.reply_to_message.as_('reply_to'),
    F.message_id != F.reply_to_message.message_id,
    StateFilter('*'),
)
async def on_bool_other_user(message: Message, reply_to: Message) -> None:
    full_name = reply_to.from_user.username or reply_to.from_user.full_name
    full_name = to_snake_case(full_name)
    text = (
        '<pre>'
        '<code class="language-python">\n'
        f'>>> bool({full_name})\n'
        f'{random.choice(("True", "False"))}'
        '</code>'
        '</pre>'
    )
    await message.answer(text)
