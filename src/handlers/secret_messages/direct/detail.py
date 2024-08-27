from aiogram import Bot, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import SecretMessageDetailCallbackData
from repositories import SecretMessageRepository
from services import can_see_secret_message, notify_secret_message_seen

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
    secret_text_message = await secret_message_repository.get_by_id(
        secret_message_id=callback_data.secret_message_id,
    )

    if not can_see_secret_message(
            user_id=callback_query.from_user.id,
            secret_text_message=secret_text_message,
    ):
        text = 'Это сообщение не предназначено для тебя 😉'
    else:
        text = secret_text_message.text
    await callback_query.answer(text, show_alert=True)

    is_recipient = (
            secret_text_message.recipient.id
            == callback_query.from_user.id
    )

    if is_recipient and not secret_text_message.is_seen:
        await secret_message_repository.mark_as_seen(secret_text_message.id)
        await notify_secret_message_seen(
            bot=bot,
            secret_text_message=secret_text_message,
        )
