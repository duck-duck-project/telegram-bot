from typing import Protocol

from aiogram.enums import ChatType
from aiogram.types import (
    Chat, URLInputFile, Update,
    User as TelegramUser,
)

__all__ = (
    'extract_user_from_update',
    'extract_chat_type_from_update_or_none',
    'get_username_or_fullname',
    'get_user_profile_photo',
    'get_chat_id_if_group_chat'
)

from pydantic import HttpUrl


class HasUsernameOrFullname(Protocol):
    fullname: str
    username: str | None


def extract_user_from_update(update: Update) -> TelegramUser:
    """Extract user from update.

    Args:
        update: Update object.

    Returns:
        User object.

    Raises:
        ValueError: If update type is unknown.
    """
    if update.message is not None:
        return update.message.from_user
    elif update.callback_query is not None:
        return update.callback_query.from_user
    elif update.inline_query is not None:
        return update.inline_query.from_user
    elif update.chosen_inline_result is not None:
        return update.chosen_inline_result.from_user
    else:
        raise ValueError('Unknown event type')


def extract_chat_type_from_update_or_none(update: Update) -> ChatType | None:
    if update.message is not None:
        return ChatType(update.message.chat.type)
    if update.callback_query is not None:
        if update.callback_query.message is not None:
            return ChatType(update.callback_query.message.chat.type)
    if update.inline_query is not None:
        return ChatType(update.inline_query.chat_type)


def get_username_or_fullname(user: HasUsernameOrFullname) -> str:
    return user.username or user.fullname


async def get_user_profile_photo(
        user: TelegramUser,
        profile_photo_url: HttpUrl | None = None,
):
    if profile_photo_url is not None:
        return URLInputFile(str(profile_photo_url))

    profile_photos = await user.get_profile_photos()
    if profile_photos.photos:
        return profile_photos.photos[0][-1].file_id

    url = (
        'https://api.thecatapi.com/v1/'
        'images/search?format=src&mime_types=jpg,png'
    )
    return URLInputFile(url)


def get_chat_id_if_group_chat(chat: Chat) -> int | None:
    if chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        return chat.id
