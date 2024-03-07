from aiogram.types import Message

__all__ = ('choices_between_options_filter',)


def choices_between_options_filter(message: Message) -> bool | dict:
    if not message.text.lower().startswith('выбери '):
        return False
    message_text = message.text[7:]

    options = message_text.split(' или ')
    return {'options': options}
