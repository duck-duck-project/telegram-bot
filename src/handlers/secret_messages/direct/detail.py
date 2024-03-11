from aiogram import Bot, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import SecretMessageDetailCallbackData
from repositories import SecretMessageRepository
from services import can_see_contact_secret, notify_secret_message_seen

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    SecretMessageDetailCallbackData.filter(),
    StateFilter('*'),
)
async def on_show_contact_message(
        callback_query: CallbackQuery,
        callback_data: SecretMessageDetailCallbackData,
        secret_message_repository: SecretMessageRepository,
        bot: Bot,
) -> None:
    secret_message = await secret_message_repository.get_by_id(
        secret_message_id=callback_data.secret_message_id,
    )

    if not can_see_contact_secret(
            user_id=callback_query.from_user.id,
            secret_message=secret_message,
    ):
        text = 'Это сообщение не предназначено для тебя 😉'
    else:
        text = secret_message.text
    await callback_query.answer(text, show_alert=True)

    is_recipient = secret_message.recipient.id == callback_query.from_user.id

    if is_recipient and not secret_message.is_seen:
        await secret_message_repository.update(
            secret_message_id=secret_message.id,
            is_seen=True,
        )
        await notify_secret_message_seen(bot=bot, secret_message=secret_message)
