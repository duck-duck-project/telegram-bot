from aiogram.enums import ChatType
from aiogram.types import Update

from middlewares.common import Handler, ContextData, HandlerReturn
from repositories import UserRepository
from services import extract_user_from_update

__all__ = ('user_retrieve_middleware',)


async def user_retrieve_middleware(
        handler: Handler,
        event: Update,
        data: ContextData,
) -> HandlerReturn:
    if event.message is not None:
        message = event.message
        is_chat_type_private = message.chat.type == ChatType.PRIVATE
        no_command = (
                message.text is not None
                and not message.text.startswith('/')
        )

        bot_id = data['bot_user'].id
        is_reply_to_bot = (
                event.message.reply_to_message is not None
                and event.message.reply_to_message.from_user.id == bot_id
        )

        if no_command and not is_chat_type_private and not is_reply_to_bot:
            return await handler(event, data)

    from_user = extract_user_from_update(event)

    user_repository: UserRepository = data['user_repository']
    user, _ = await user_repository.upsert(
        user_id=from_user.id,
        fullname=from_user.full_name,
        username=from_user.username,
    )
    data['user'] = user
    return await handler(event, data)
