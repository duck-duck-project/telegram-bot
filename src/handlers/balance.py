from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from repositories import UserRepository
from views import UserBalanceView, answer_view

router = Router(name=__name__)


@router.callback_query(
    F.data == 'show-user-balance',
    StateFilter('*'),
)
async def on_show_user_balance(
        callback_query: CallbackQuery,
        user_repository: UserRepository,
) -> None:
    user_id = callback_query.from_user.id
    user_balance = await user_repository.get_balance(user_id)
    view = UserBalanceView(user_balance)
    await answer_view(message=callback_query.message, view=view)
    await callback_query.answer()