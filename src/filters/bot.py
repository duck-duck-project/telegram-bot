from aiogram.types import Message, User

__all__ = ('reply_message_from_bot_filter',)


async def reply_message_from_bot_filter(
        message: Message,
        bot_user: User,
) -> bool:
    return message.reply_to_message.from_user.id == bot_user.id
