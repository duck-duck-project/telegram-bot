from aiogram import F, Router
from aiogram.filters import StateFilter, and_f, or_f
from aiogram.types import Message, URLInputFile

from repositories import UserRepository
from views import ProfileView, answer_photo_view

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
        user_repository: UserRepository,
        reply_to_message: Message | None = None,
) -> None:
    from_user = (
        reply_to_message.from_user
        if reply_to_message is not None
        else message.from_user
    )
    user = await user_repository.get_by_id(from_user.id)

    profile_photos = await from_user.get_profile_photos()
    if not profile_photos.photos:
        url = (
            'https://api.thecatapi.com/v1/'
            'images/search?format=src&mime_types=jpg,png'
        )
        photo = URLInputFile(url)
    else:
        photo = profile_photos.photos[0][-1].file_id

    view = ProfileView(user, photo)

    await answer_photo_view(message=message, view=view)
