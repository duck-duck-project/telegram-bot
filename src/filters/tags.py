from aiogram.types import Message

from enums import TagWeight

__all__ = ('tag_filter',)


def tag_filter(message: Message) -> dict | bool:
    try:
        command, text = message.text.splitlines()
    except ValueError:
        return False

    command_to_weight = {
        'дать тег золото': TagWeight.GOLD,
        'дать тег серебро': TagWeight.SILVER,
        'дать тег бронза': TagWeight.BRONZE,
    }

    try:
        weight = command_to_weight[command.lower()]
    except KeyError:
        return False

    if command.lower() != 'дать тэг':
        return False

    of_user_id = message.from_user.id
    to_user_id = message.reply_to_message.from_user.id
    return {
        'of_user_id': of_user_id,
        'to_user_id': to_user_id,
        'text': text,
        'weight': weight,
    }
