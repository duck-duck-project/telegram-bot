import contextlib
from uuid import UUID

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from exceptions import InvalidSecretMediaDeeplinkError
from models import SecretMediaMessage, SecretTextMessage
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
        secret_media: SecretMediaMessage,
) -> bool:
    return user_id in (
        secret_media.sender.id,
        secret_media.recipient.id,
    )


def can_see_secret_message(
        *,
        user_id: int,
        secret_text_message: SecretTextMessage,
) -> bool:
    return user_id in (
        secret_text_message.sender.id,
        secret_text_message.recipient.id,
    )


def extract_secret_media_id(deep_link: str) -> UUID:
    try:
        return UUID(deep_link.split('-')[-1])
    except (ValueError, IndexError):
        raise InvalidSecretMediaDeeplinkError


async def notify_secret_message_seen(
        secret_text_message: SecretTextMessage,
        bot: Bot,
):
    view = SecretMessageReadConfirmationView(secret_text_message)
    with contextlib.suppress(TelegramAPIError):
        await bot.send_message(
            chat_id=secret_text_message.sender.id,
            text=view.get_text(),
        )
