from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from repositories import TagRepository
from views import TagListView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower() == 'награды',
    StateFilter('*'),
)
async def on_show_tags_list(
        message: Message,
        tag_repository: TagRepository,
) -> None:
    if message.reply_to_message is not None:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user

    tags = await tag_repository.get_all_by_user_id(user.id)
    view = TagListView(tags=tags, user=user)
    await answer_view(message=message, view=view)
