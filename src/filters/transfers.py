from uuid import UUID

from aiogram.types import Message

__all__ = ('transfer_operation_filter', 'transfer_rollback_filter')


def transfer_rollback_filter(message: Message) -> bool | dict:
    lines = message.reply_to_message.text.splitlines()
    last_line = lines[-1]
    transfer_id = last_line.removeprefix('🆔 Номер перевода: ')
    try:
        transfer_id = UUID(transfer_id)
    except ValueError:
        return False
    return {'transfer_id': transfer_id}


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
        amount = int(amount)
    except ValueError:
        return False

    return {'amount': amount, 'description': description}
