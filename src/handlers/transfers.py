from aiogram import Router, F
from aiogram.filters import (
    StateFilter,
    Command,
    invert_f,
    or_f,
    and_f,
    ExceptionTypeFilter,
)
from aiogram.types import Message, ErrorEvent

from exceptions import InsufficientFundsForTransferError
from filters import transfer_operation_filter
from repositories import BalanceRepository
from services import BalanceNotifier

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(InsufficientFundsForTransferError))
async def on_insufficient_funds_for_transfer_error(event: ErrorEvent) -> None:
    await event.update.message.reply(
        '❌ Недостаточно средств для перевода\n'
        '💸 Начните работать прямо сейчас /work'
    )


@router.message(
    Command('send'),
    invert_f(transfer_operation_filter),
    StateFilter('*'),
)
async def on_transfer_operation_amount_invalid(
        message: Message,
) -> None:
    await message.reply(
        '💳 Отправить перевод:\n'
        '<code>/send {сумма перевода} {описание (необязательно)}</code>'
    )


@router.message(
    F.reply_to_message,
    Command('send'),
    invert_f(F.reply_to_message.from_user.is_bot),
    transfer_operation_filter,
    StateFilter('*'),
)
async def on_create_transfer_in_group_chat(
        message: Message,
        amount: int,
        description: str | None,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    sender_id = message.from_user.id
    recipient_id = message.reply_to_message.from_user.id

    description = description or f'Transfer from {message.from_user.full_name}'

    transfer = await balance_repository.create_transfer(
        sender_id=sender_id,
        recipient_id=recipient_id,
        amount=amount,
        description=description,
    )
    await message.reply(
        text=f'✅ Перевод на сумму в {amount} дак-дак коинов успешно выполнен',
    )
    await balance_notifier.send_transfer_notification(transfer)
