from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from enums import TagWeight
from filters.tags import tag_filter
from repositories import BalanceRepository, TagRepository
from services import BalanceNotifier
from views import TagGivenView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.reply_to_message,
    F.text,
    tag_filter,
    StateFilter('*'),
)
async def on_create_tag(
        message: Message,
        tag_repository: TagRepository,
        of_user_id: int,
        to_user_id: int,
        text: str,
        weight: TagWeight,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    weight_to_price = {
        TagWeight.GOLD: 1000,
        TagWeight.SILVER: 100,
        TagWeight.BRONZE: 10,
    }
    price = weight_to_price[weight]

    await tag_repository.create(
        of_user_id=of_user_id,
        to_user_id=to_user_id,
        text=text,
        weight=weight,
    )
    withdrawal = await balance_repository.create_withdrawal(
        user_id=of_user_id,
        amount=price,
        description='Выдача тэга',
    )
    await balance_notifier.send_withdrawal_notification(withdrawal)
    await answer_view(message=message, view=TagGivenView())
