from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import TagDeleteCallbackData
from repositories import TagRepository

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
) -> None:
    await tag_repository.delete(
        user_id=callback_query.from_user.id,
        tag_id=callback_data.tag_id,
    )
    await callback_query.answer(text='❗️ Награда продана', show_alert=True)
    await callback_query.message.delete_reply_markup()
