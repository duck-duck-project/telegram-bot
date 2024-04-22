from datetime import datetime

from aiogram.types import Message

__all__ = ('birth_date_filter',)


def birth_date_filter(message: Message) -> bool | dict:
    try:
        command, birth_date = message.text.lower().splitlines()
    except ValueError:
        return False

    if command != 'дата рождения':
        return False

    try:
        birth_date = datetime.strptime(birth_date, '%d.%m.%Y')
    except ValueError:
        return False

    return {'birth_date': birth_date.date()}
