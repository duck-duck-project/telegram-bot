from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, User as TelegramUser

from enums import TagWeight
from filters.tags import tag_create_command_filter
from repositories import BalanceRepository, TagRepository, UserRepository
from services import BalanceNotifier
from services.tags import compute_tag_issue_price
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
        of_user: TelegramUser,
        to_user: TelegramUser,
        text: str,
        weight: TagWeight,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
        user_repository: UserRepository,
) -> None:
    user, _ = await user_repository.upsert(
        user_id=message.from_user.id,
        username=message.from_user.username,
        fullname=message.from_user.full_name,
    )
    price = compute_tag_issue_price(
        tag_weight=weight,
        is_premium=user.is_premium,
    )
    withdrawal = await balance_repository.create_withdrawal(
        user_id=of_user.id,
        amount=price,
        description='Выдача награды',
    )
    await balance_notifier.send_withdrawal_notification(withdrawal)
    await answer_view(message=message, view=TagGivenView(to_user))
    await tag_repository.create(
        of_user_id=of_user.id,
        to_user_id=to_user.id,
        text=text,
        weight=weight,
    )
