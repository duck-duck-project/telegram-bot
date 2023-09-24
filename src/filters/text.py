from aiogram.types import Message

__all__ = ('integer_filter',)


def integer_filter(message: Message) -> bool | dict:
    """Filter that checks if message text is integer."""
    try:
        return {'number': int(message.text)}
    except ValueError:
        return False
