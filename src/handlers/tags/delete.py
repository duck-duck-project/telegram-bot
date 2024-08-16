from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import TagDeleteCallbackData
from models import User
from repositories import BalanceRepository, TagRepository
from services import BalanceNotifier, compute_tag_refund_price

__all__ = ('Router',)

router = Router(name=__name__)


@router.callback_query(
    TagDeleteCallbackData.filter(),
    StateFilter('*'),
)
async def on_delete_tag(
        callback_query: CallbackQuery,
        tag_repository: TagRepository,
        callback_data: TagDeleteCallbackData,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
        user: User,
) -> None:
    await tag_repository.delete(
        user_id=callback_query.from_user.id,
        tag_id=callback_data.tag_id,
    )
    await callback_query.answer(text='❗️ Награда продана', show_alert=True)
    await callback_query.message.delete_reply_markup()
    price = compute_tag_refund_price(
        tag_weight=callback_data.tag_weight,
        is_premium=user.is_premium,
    )
    deposit = await balance_repository.create_deposit(
        user_id=callback_query.from_user.id,
        amount=price,
        description='🏅 Продажа награды',
    )
    await balance_notifier.send_deposit_notification(deposit)
