from aiogram.types import Message

from services import parse_abbreviated_number

__all__ = ('transfer_operation_filter',)


def transfer_operation_filter(message: Message) -> bool | dict:
    args = message.text.split()
    if len(args) < 2:
        return False
    if len(args) == 2:
        _, amount = args
        description = None
    else:
        _, amount, *description = args
        description = ' '.join(description)

    try:
        amount = parse_abbreviated_number(amount)
    except ValueError:
        return False

    return {'amount': amount, 'description': description}
