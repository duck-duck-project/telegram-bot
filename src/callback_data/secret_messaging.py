from uuid import UUID

from aiogram.filters.callback_data import CallbackData

__all__ = (
    'SecretMessageDetailCallbackData',
    'SecretMessageDeleteCallbackData',
)


class SecretMessageDetailCallbackData(
    CallbackData,
    prefix='secret-message-detail',
):
    secret_message_id: UUID


class SecretMessageDeleteCallbackData(
    CallbackData,
    prefix='secret-message-delete',
):
    secret_message_id: UUID
