from aiogram import Bot
from aiogram.types import Message

__all__ = ('reply_message_from_bot_filter',)


async def reply_message_from_bot_filter(
        message: Message,
        bot: Bot,
) -> bool:
    return message.reply_to_message.from_user.id == bot.id
