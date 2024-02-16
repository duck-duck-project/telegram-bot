from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import Message

from exceptions import (
    ThemeDoesNotExistError,
)
from filters import theme_update_command_filter
from models import User
from repositories import BalanceRepository, UserRepository
from repositories.themes import ThemeRepository
from services import BalanceNotifier
from views import ThemeSuccessfullyUpdatedView, answer_view

__all__ = ('register_handlers',)


async def on_update_user_theme(
        message: Message,
        user: User,
        user_repository: UserRepository,
        theme_repository: ThemeRepository,
        balance_repository: BalanceRepository,
        theme_id: int,
        balance_notifier: BalanceNotifier,
) -> None:
    theme = await theme_repository.get_by_id(theme_id)

    if theme.is_hidden:
        raise ThemeDoesNotExistError

    profile_photo_url = user.profile_photo_url
    if profile_photo_url is not None:
        profile_photo_url = str(profile_photo_url)

    await user_repository.upsert(
        user_id=user.id,
        fullname=user.fullname,
        username=user.username,
        can_be_added_to_contacts=user.can_be_added_to_contacts,
        secret_messages_theme_id=theme_id,
        can_receive_notifications=user.can_receive_notifications,
        profile_photo_url=profile_photo_url,
    )

    withdrawal = await balance_repository.create_withdrawal(
        user_id=user.id,
        amount=1000,
        description='🎨 Theme change',
    )
    view = ThemeSuccessfullyUpdatedView()
    await answer_view(message=message, view=view)
    await balance_notifier.send_withdrawal_notification(withdrawal)


def register_handlers(router: Router) -> None:
    router.message.register(
        on_update_user_theme,
        theme_update_command_filter,
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
