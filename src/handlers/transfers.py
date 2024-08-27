from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import (
    Command,
    ExceptionTypeFilter,
    StateFilter,
    invert_f,
    or_f,
)
from aiogram.types import CallbackQuery, ErrorEvent, Message

from callback_data import TransferRollbackCallbackData
from exceptions import (
    InsufficientFundsForTransferError,
    InsufficientFundsForTransferRollbackError,
    TransactionDoesNotBelongToUserError,
    TransactionDoesNotExistError,
    TransferRollbackExpiredError,
)
from filters import transfer_operation_filter
from repositories import BalanceRepository
from services import BalanceNotifier
from views import (
    TransferExecutedView,
    reply_view,
)

router = Router(name=__name__)


@router.callback_query(
    TransferRollbackCallbackData.filter(),
    StateFilter('*'),
)
async def on_rollback_transfer(
        callback_query: CallbackQuery,
        callback_data: TransferRollbackCallbackData,
        balance_repository: BalanceRepository,
) -> None:
    try:
        await balance_repository.rollback_transfer(
            transfer_id=callback_data.transfer_id,
            user_id=callback_query.from_user.id,
        )
    except InsufficientFundsForTransferRollbackError:
        await callback_query.answer(
            text='❌ Недостаточно средств у получателя для отмены перевода',
            show_alert=True,
        )
    except TransactionDoesNotBelongToUserError:
        await callback_query.answer(
            text='❌ Вы не являетесь отправителем перевода',
            show_alert=True,
        )
    except TransferRollbackExpiredError:
        await callback_query.answer(
            text='❌ Перевод может быть отменён только в течение 10 минут',
            show_alert=True,
        )
    except TransactionDoesNotExistError:
        await callback_query.answer(
            text='❌ Перевод не найден',
            show_alert=True,
        )
    else:
        await callback_query.message.delete_reply_markup()
        await callback_query.message.edit_text(
            text=f'{callback_query.message.text}\n\n<i>[Отменён]</i>'
        )


@router.error(ExceptionTypeFilter(InsufficientFundsForTransferError))
async def on_insufficient_funds_for_transfer_error(event: ErrorEvent) -> None:
    await event.update.message.reply(
        '❌ Недостаточно средств для перевода\n'
        '💸 Начните работать прямо сейчас /work'
    )


@router.message(
    Command('send'),
    invert_f(transfer_operation_filter),
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
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
    Command('send'),
    F.from_user.id == F.reply_to_message.from_user.id,
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    StateFilter('*'),
)
async def on_transfer_to_himself(message: Message) -> None:
    await message.reply('🤨 Нельзя переводить самому себе')


@router.message(
    F.reply_to_message,
    or_f(
        Command('send'),
        F.text.lower().startswith('pay '),
        F.text.lower().startswith('отправить '),
        F.text.lower().startswith('send '),
    ),
    invert_f(F.reply_to_message.from_user.is_bot),
    F.from_user.id != F.reply_to_message.from_user.id,
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
    view = TransferExecutedView(transfer)
    await reply_view(message=message, view=view)
    await balance_notifier.send_transfer_notification(transfer)
