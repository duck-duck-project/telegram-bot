from aiogram.types import Message

from enums import Gender

__all__ = ('gender_filter', 'TEXT_TO_GENDER')

TEXT_TO_GENDER = {
    'женский': Gender.FEMALE,
    'мужской': Gender.MALE,
    'другой': Gender.OTHER,
}


def gender_filter(message: Message) -> bool | dict:
    if message.text is None:
        return False

    try:
        command, gender = message.text.splitlines()
    except ValueError:
        return False

    if command.strip().lower() != 'поменять пол':
        return False

    if gender not in TEXT_TO_GENDER:
        return False

    return {'gender': TEXT_TO_GENDER[gender]}
