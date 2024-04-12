from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import TagDeleteCallbackData
from repositories import BalanceRepository, TagRepository
from services import BalanceNotifier, TAG_WEIGHT_TO_PRICE

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
) -> None:
    price = TAG_WEIGHT_TO_PRICE[callback_data.tag_weight]
    deposit = await balance_repository.create_deposit(
        user_id=callback_query.from_user.id,
        amount=price // 2,
        description='🏅 Продажа награды',
    )
    await balance_notifier.send_deposit_notification(deposit)
    await tag_repository.delete(
        user_id=callback_query.from_user.id,
        tag_id=callback_data.tag_id,
    )
    await callback_query.answer(text='❗️ Награда продана', show_alert=True)
    await callback_query.message.delete_reply_markup()
