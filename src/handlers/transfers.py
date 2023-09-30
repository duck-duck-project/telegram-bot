from aiogram import Router, F
from aiogram.filters import StateFilter, Command, invert_f, or_f, and_f
from aiogram.types import Message

from filters import transfer_operation_filter
from repositories import BalanceRepository
from services import PrivateChatNotifier

router = Router(name=__name__)


@router.message(
    or_f(
        Command('send'),
        and_f(
            Command('pay'),
            invert_f(transfer_operation_filter),
        )
    ),
    StateFilter('*'),
)
async def on_transfer_operation_amount_invalid(
        message: Message,
) -> None:
    await message.reply(
        '💳 Отправить перевод:\n'
        '<code>/pay {сумма перевода} {описание (необязательно)}</code>'
    )


@router.message(
    F.reply_to_message,
    Command('pay'),
    invert_f(F.reply_to_message.from_user.is_bot),
    transfer_operation_filter,
    StateFilter('*'),
)
async def on_create_transfer_in_group_chat(
        message: Message,
        amount: int,
        description: str | None,
        balance_repository: BalanceRepository,
        private_chat_notifier: PrivateChatNotifier,
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
    await private_chat_notifier.send_transfer_notification(transfer)
