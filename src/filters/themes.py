from uuid import UUID

from aiogram.types import Message

__all__ = ('theme_update_command_filter',)


def theme_update_command_filter(message: Message) -> bool | dict:
    try:
        _, theme_id = message.text.split('_')
        theme_id = UUID(theme_id)
    except ValueError:
        return False
    return {'theme_id': theme_id}
