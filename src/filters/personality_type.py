from aiogram.types import Message

from enums import PersonalityTypePrefix, PersonalityTypeSuffix

__all__ = ('personality_type_filter',)


def personality_type_filter(message: Message) -> dict | bool:
    try:
        command, personality_type = message.text.lower().splitlines()
    except ValueError:
        return False

    if command.strip() != 'тип личности':
        return False

    try:
        prefix, suffix = [part.upper() for part in personality_type.split('-')]
        prefix = PersonalityTypePrefix(prefix)
        suffix = PersonalityTypeSuffix(suffix)
    except ValueError:
        return False

    return {
        'personality_type_prefix': prefix,
        'personality_type_suffix': suffix,
    }
