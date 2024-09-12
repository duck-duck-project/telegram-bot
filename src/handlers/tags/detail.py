from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters.tags import tag_detail_command_filter
from repositories import TagRepository
from services import find_tag_by_number
from views import TagDetailView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text,
    tag_detail_command_filter,
    StateFilter('*'),
)
async def on_show_tag_detail(
        message: Message,
        tag_repository: TagRepository,
        tag_number: int,
) -> None:
    user_tags = await tag_repository.get_all_by_user_id(message.from_user.id)
    tag = find_tag_by_number(tags=user_tags.tags, number=tag_number)
    view = TagDetailView(tag, to_user=message.from_user)
    await answer_view(message=message, view=view)
