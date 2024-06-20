from aiogram.types import Message

__all__ = ('sport_activity_filter',)


def sport_activity_filter(
        message: Message,
) -> bool | dict:
    if message.text is None:
        return False

    if not message.text.lower().startswith('заняться спортом '):
        return False

    sport_activity_name = message.text[16:].strip()

    return {'sport_activity_name': sport_activity_name}
