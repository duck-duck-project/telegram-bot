from aiogram.types import Message

from enums import TagWeight

__all__ = ('tag_create_command_filter', 'tag_detail_command_filter')


def tag_detail_command_filter(message: Message) -> dict | bool:
    try:
        command, tag_number = message.text.split(' ')
    except ValueError:
        return False

    if command.lower() != 'награда':
        return False

    try:
        return {'tag_number': int(tag_number)}
    except ValueError:
        return False


def tag_create_command_filter(message: Message) -> dict | bool:
    try:
        command, text = message.text.splitlines()
    except ValueError:
        return False

    command_to_weight = {
        'наградить золотом': TagWeight.GOLD,
        'наградить серебром': TagWeight.SILVER,
        'наградить бронзой': TagWeight.BRONZE,
    }

    try:
        weight = command_to_weight[command.lower().strip()]
    except KeyError:
        return False

    of_user = message.from_user
    to_user = message.reply_to_message.from_user
    return {
        'of_user': of_user,
        'to_user': to_user,
        'text': text,
        'weight': weight,
    }
