import contextlib
from typing import Iterable
from uuid import UUID

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from exceptions import InvalidSecretMediaDeeplinkError
from models import HasUserId, SecretMessage

__all__ = (
    'can_see_team_secret',
    'can_see_contact_secret',
    'extract_secret_media_id',
    'notify_secret_message_seen',
)


def can_see_team_secret(
        *,
        user_id: int,
        team_members: Iterable[HasUserId],
) -> bool:
    user_ids = {member.user_id for member in team_members}
    return user_id in user_ids


def can_see_contact_secret(
        *,
        user_id: int,
        secret_message: SecretMessage,
) -> bool:
    return user_id in (
        secret_message.sender.id,
        secret_message.recipient.id,
    )


def extract_secret_media_id(deep_link: str) -> UUID:
    try:
        return UUID(deep_link.split('-')[-1])
    except (ValueError, IndexError):
        raise InvalidSecretMediaDeeplinkError


async def notify_secret_message_seen(
        secret_message: SecretMessage,
        bot: Bot,
):
    with contextlib.suppress(TelegramAPIError):
        await bot.send_message(
            chat_id=secret_message.sender.id,
            text=f'✅ Сообщение прочитано\n\n<i>{secret_message.text}</i>',
        )
