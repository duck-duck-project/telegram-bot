from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, User as TelegramUser

from enums import TagWeight
from filters.tags import tag_create_command_filter
from repositories import TagRepository
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
) -> None:
    await tag_repository.create(
        of_user_id=of_user.id,
        to_user_id=to_user.id,
        text=text,
        weight=weight,
    )
    await answer_view(message=message, view=TagGivenView(to_user))
