from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from callback_data import TagListCallbackData
from repositories import TagRepository
from views import TagListView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    TagListCallbackData.filter(),
    StateFilter('*'),
)
async def on_show_tag_list_callback(
        callback_query: CallbackQuery,
        callback_data: TagListCallbackData,
        tag_repository: TagRepository,
) -> None:
    tags = await tag_repository.get_all_by_user_id(callback_data.user_id)
    view = TagListView(tags=tags, user=callback_query.from_user)
    await answer_view(message=callback_query.message, view=view)
    await callback_query.answer()


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
