from aiogram.types import Message

__all__ = ('medicine_filter',)


def medicine_filter(message: Message) -> dict | bool:
    if message.text is None:
        return False

    if not message.text.lower().startswith('лекарство '):
        return False

    medicine_name = message.text[10:]

    return {'medicine_name': medicine_name}
