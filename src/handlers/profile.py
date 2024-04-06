from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter, and_f, or_f
from aiogram.types import Message, URLInputFile

from models import User
from repositories import UserRepository
from views import ProfileView, answer_media_group_view

router = Router(name=__name__)


@router.message(
    or_f(
        and_f(
            F.text.lower().in_({'кто ты', 'ты кто'}),
            F.reply_to_message.as_('reply_to_message'),
        ),
        F.text.lower().in_({'кто я', 'профиль', 'id', 'мой id', 'паспорт'}),
    ),
    StateFilter('*'),
)
async def on_show_profile(
        message: Message,
        user: User,
        user_repository: UserRepository,
        reply_to_message: Message | None = None,
) -> None:
    if reply_to_message is not None:
        from_user = reply_to_message.from_user
        user = await user_repository.get_by_id(reply_to_message.from_user.id)
    else:
        from_user = message.from_user

    profile_photos = await from_user.get_profile_photos()
    if not profile_photos.photos:
        url = (
            'https://api.thecatapi.com/v1/'
            'images/search?format=src&mime_types=jpg,png'
        )
        photos = [URLInputFile(url)]
    else:
        photos = [photo[-1].file_id for photo in profile_photos.photos[:10]]

    view = ProfileView(user, photos)

    try:
        await answer_media_group_view(message=message, view=view)
    except TelegramBadRequest:
        view = ProfileView(user, photos[:1])
        await answer_media_group_view(message=message, view=view)
