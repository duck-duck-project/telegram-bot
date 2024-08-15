from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from callback_data import TagListCallbackData
from repositories import TagRepository
from services.clean_up import CleanUpService
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
        clean_up_service: CleanUpService,
) -> None:
    tags = await tag_repository.get_all_by_user_id(callback_data.user_id)
    view = TagListView(tags=tags, user_full_name=callback_data.user_full_name)
    sent_message = await answer_view(message=callback_query.message, view=view)
    await callback_query.answer()
    if callback_data.user_id == 784163357:
        sent_media = await sent_message.reply_animation(
            'https://i.imgur.com/Zo2yiaG.mp4',
        )
    elif callback_data.user_id == 5777421574:
        sent_media = await sent_message.reply_photo(
            'https://i.imgur.com/sre1G1c.jpeg',
        )
    else:
        return
    await clean_up_service.create_clean_up_task(
        callback_query.message,
        sent_message,
        sent_media,
    )


@router.message(
    F.text.lower() == 'награды',
    StateFilter('*'),
)
async def on_show_tags_list(
        message: Message,
        tag_repository: TagRepository,
        clean_up_service: CleanUpService,
) -> None:
    if message.reply_to_message is not None:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user

    tags = await tag_repository.get_all_by_user_id(user.id)
    view = TagListView(tags=tags, user_full_name=user.full_name)
    sent_message = await answer_view(message=message, view=view)
    if user.id == 784163357:
        sent_media = await sent_message.reply_animation(
            'https://i.imgur.com/Zo2yiaG.mp4',
        )
    elif user.id == 5777421574:
        sent_media = await sent_message.reply_photo(
            'https://i.imgur.com/sre1G1c.jpeg',
        )
    else:
        return
    await clean_up_service.create_clean_up_task(
        message,
        sent_message,
        sent_media,
    )

