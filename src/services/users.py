from typing import Protocol

from aiogram.enums import ChatType
from aiogram.types import Update, User

__all__ = (
    'extract_user_from_update',
    'extract_chat_type_from_update_or_none',
    'get_username_or_fullname',
)


class HasUsernameOrFullname(Protocol):
    fullname: str
    username: str | None


def extract_user_from_update(update: Update) -> User:
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
