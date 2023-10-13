from uuid import UUID

from aiogram.filters.callback_data import CallbackData

__all__ = (
    'SecretMessageDetailCallbackData',
    'InvertedSecretMessageDetailCallbackData',
    'SecretMessageForTeamCallbackData',
)


class InvertedSecretMessageDetailCallbackData(
    CallbackData,
    prefix='inverted-whisp',
):
    contact_id: int
    secret_message_id: UUID


class SecretMessageDetailCallbackData(CallbackData, prefix='show-whisp'):
    contact_id: int
    secret_message_id: UUID


class SecretMessageForTeamCallbackData(
    CallbackData,
    prefix='secret-message-team',
):
    team_id: int
    secret_message_id: UUID
