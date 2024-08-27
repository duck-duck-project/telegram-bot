from aiogram import F, Router
from aiogram.filters import (
    Command, ExceptionTypeFilter, StateFilter, invert_f, or_f,
)
from aiogram.types import CallbackQuery, ErrorEvent, Message, User

from callback_data import UserBalanceDetailCallbackData
from exceptions import InsufficientFundsForWithdrawalError
from repositories import BalanceRepository
from services import int_gaps
from views import (
    UserBalanceView,
    UserBalanceWithoutNameView,
    answer_view,
)

router = Router(name=__name__)


@router.error(
    ExceptionTypeFilter(InsufficientFundsForWithdrawalError),
    StateFilter('*'),
)
async def on_insufficient_funds_for_withdrawal_error(event: ErrorEvent) -> None:
    text = (
        '❌ Недостаточно средств для списания\n'
        f'💸 Необходимо {int_gaps(event.exception.amount)} дак-дак коинов'
    )
    if event.update.message is not None:
        await event.update.message.reply(text)
    if event.update.callback_query is not None:
        await event.update.callback_query.answer(text, show_alert=True)


@router.message(
    or_f(
        Command('balance'),
        F.text.lower().in_({'баланс', 'balance', '💰 мой баланс'}),
    ),
    or_f(
        F.reply_to_message.from_user.as_('from_user'),
        F.from_user.as_('from_user'),
    ),
    invert_f(F.reply_to_message.is_bot),
    StateFilter('*'),
)
async def on_show_other_user_balance(
        message: Message,
        from_user: User,
        balance_repository: BalanceRepository,
) -> None:
    user_balance = await balance_repository.get_user_balance(from_user.id)
    view = UserBalanceView(user_balance, from_user.full_name)
    await answer_view(message=message, view=view)


@router.callback_query(
    UserBalanceDetailCallbackData.filter(),
    StateFilter('*'),
)
async def on_show_user_balance(
        callback_query: CallbackQuery,
        callback_data: UserBalanceDetailCallbackData,
        balance_repository: BalanceRepository,
) -> None:
    user_balance = await balance_repository.get_user_balance(
        callback_data.user_id
    )
    view = UserBalanceWithoutNameView(balance=user_balance.balance)
    await callback_query.answer(view.get_text(), show_alert=True)

