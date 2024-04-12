from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, User

from enums import TagWeight
from filters.tags import tag_create_command_filter
from repositories import BalanceRepository, TagRepository
from services import BalanceNotifier, TAG_WEIGHT_TO_PRICE
from views import TagGivenView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.reply_to_message,
    F.text,
    tag_create_command_filter,
    StateFilter('*'),
)
async def on_create_tag(
        message: Message,
        tag_repository: TagRepository,
        of_user: User,
        to_user: User,
        text: str,
        weight: TagWeight,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    price = TAG_WEIGHT_TO_PRICE[weight]

    await tag_repository.create(
        of_user_id=of_user.id,
        to_user_id=to_user.id,
        text=text,
        weight=weight,
    )
    withdrawal = await balance_repository.create_withdrawal(
        user_id=of_user.id,
        amount=price,
        description='Выдача награды',
    )
    await balance_notifier.send_withdrawal_notification(withdrawal)
    await answer_view(message=message, view=TagGivenView(to_user))
