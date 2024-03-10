from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import SecretMessageDeleteCallbackData
from repositories import SecretMessageRepository

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    SecretMessageDeleteCallbackData.filter(),
    StateFilter('*'),
)
async def on_delete_secret_message(
        callback_query: CallbackQuery,
        callback_data: SecretMessageDeleteCallbackData,
        secret_message_repository: SecretMessageRepository,
) -> None:
    secret_message = await secret_message_repository.get_by_id(
        secret_message_id=callback_data.secret_message_id,
    )
    if secret_message.sender_id != callback_query.from_user.id:
        await callback_query.answer(
            '❌ Вы не можете удалить это сообщение',
            show_alert=True,
        )
        return
    await secret_message_repository.delete_by_id(
        secret_message_id=callback_data.secret_message_id,
    )
    await callback_query.answer('✅ Сообщение удалено', show_alert=True)
