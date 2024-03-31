import contextlib
from uuid import UUID

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from exceptions import InvalidSecretMediaDeeplinkError
from models import SecretMedia, SecretMessage
from views.secret_messaging import SecretMessageReadConfirmationView

__all__ = (
    'can_see_secret_message',
    'extract_secret_media_id',
    'notify_secret_message_seen',
    'can_see_secret_media',
)


def can_see_secret_media(
        *,
        user_id: int,
        secret_media: SecretMedia,
) -> bool:
    return user_id in (
        secret_media.contact.of_user.id,
        secret_media.contact.to_user.id,
    )


def can_see_secret_message(
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
    view = SecretMessageReadConfirmationView(secret_message)
    with contextlib.suppress(TelegramAPIError):
        await bot.send_message(
            chat_id=secret_message.sender.id,
            text=view.get_text(),
        )
