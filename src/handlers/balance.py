from aiogram import Router, F
from aiogram.filters import StateFilter, Command, ExceptionTypeFilter, or_f
from aiogram.types import CallbackQuery, Message, ErrorEvent

from exceptions import InsufficientFundsForWithdrawalError
from repositories import BalanceRepository
from services import BalanceNotifier
from views import (
    UserBalanceView,
    render_message_or_callback_query,
    FinanceMenuView,
    answer_view,
)

router = Router(name=__name__)


@router.message(
    F.text == '💰 Финансы',
    StateFilter('*'),
)
async def on_show_finance_menu(message: Message) -> None:
    view = FinanceMenuView()
    await answer_view(message=message, view=view)


@router.error(ExceptionTypeFilter(InsufficientFundsForWithdrawalError))
async def on_insufficient_funds_for_withdrawal_error(event: ErrorEvent) -> None:
    text = (
        '❌ Недостаточно средств для списания\n'
        f'💸 Необходимо {event.exception.amount} дак-дак коинов'
    )
    if event.update.message is not None:
        await event.update.message.reply(text)
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(text, show_alert=True)


@router.message(
    Command('balance'),
    F.reply_to_message.as_('reply'),
    StateFilter('*'),
)
async def on_show_other_user_balance(
        message: Message,
        reply: Message,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    withdrawal = await balance_repository.create_withdrawal(
        user_id=message.from_user.id,
        amount=100,
        description='Просмотр чужого баланса',
    )
    await balance_notifier.send_withdrawal_notification(withdrawal)
    user_id = reply.from_user.id
    user_balance = await balance_repository.get_user_balance(user_id)
    view = UserBalanceView(user_balance)
    await answer_view(message=message, view=view)


@router.message(
    or_f(
        Command('balance'),
        F.text == '💰 Мой баланс',
    ),
    StateFilter('*'),
)
@router.callback_query(
    F.data == 'show-user-balance',
    StateFilter('*'),
)
async def on_show_user_balance(
        message_or_callback_query: Message | CallbackQuery,
        balance_repository: BalanceRepository,
) -> None:
    user_id = message_or_callback_query.from_user.id
    user_balance = await balance_repository.get_user_balance(user_id)
    view = UserBalanceView(user_balance)
    await render_message_or_callback_query(
        message_or_callback_query=message_or_callback_query,
        view=view,
    )


@router.message(
    Command('richest_top'),
    StateFilter('*'),
)
async def on_show_richest_users_statistics(
        message: Message,
        balance_repository: BalanceRepository,
) -> None:
    await balance_repository.create_richest_users_statistics_task(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
    )
