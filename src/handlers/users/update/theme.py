from uuid import UUID

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import Message

from exceptions import ThemeDoesNotExistError
from filters import theme_update_command_filter
from models import User
from repositories import UserRepository
from repositories.themes import ThemeRepository
from views import ThemeSuccessfullyUpdatedView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text,
    theme_update_command_filter,
    F.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
async def on_update_user_theme(
        message: Message,
        user: User,
        user_repository: UserRepository,
        theme_repository: ThemeRepository,
        theme_id: UUID,
) -> None:
    theme = await theme_repository.get_by_id(theme_id)

    if theme.is_hidden:
        raise ThemeDoesNotExistError

    await user_repository.upsert(
        user_id=user.id,
        fullname=user.fullname,
        username=user.username,
        theme_id=theme_id,
    )
    view = ThemeSuccessfullyUpdatedView()
    await answer_view(message=message, view=view)
