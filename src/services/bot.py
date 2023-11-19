import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

__all__ = ('try_to_delete_message',)

logger = logging.getLogger(__name__)


async def try_to_delete_message(message: Message) -> bool:
    try:
        return await message.delete()
    except TelegramBadRequest:
        logger.warning(f'Could not delete message in chat {message.chat.id}')
        return False
