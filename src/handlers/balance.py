from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.types import CallbackQuery, Message

from repositories import BalanceRepository
from views import UserBalanceView, render_message_or_callback_query

router = Router(name=__name__)


@router.message(
    Command('balance'),
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
