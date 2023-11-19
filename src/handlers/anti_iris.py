from aiogram import Router, F
from aiogram.types import Message

from services import try_to_delete_message

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.from_user.username == '@iris_moon_bot',
)
async def on_message_from_iris_bot(
        message: Message,
        words_in_blacklist: set[str],
):
    message_text = message.text.lower()
    for word_in_blacklist in words_in_blacklist:
        if word_in_blacklist in message_text:
            await try_to_delete_message(message)
            break

    if message.reply_to_message is not None:
        await try_to_delete_message(message.reply_to_message)
