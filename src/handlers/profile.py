from aiogram import F, Router
from aiogram.filters import StateFilter, and_f, or_f
from aiogram.types import Message, URLInputFile

from repositories import UserRepository
from views import ProfileView, answer_photo_view

router = Router(name=__name__)


@router.message(
    or_f(
        and_f(
            F.text.lower().in_({
                'кто ты',
                'ты кто',
                'id',
                'ид',
            }),
            F.reply_to_message,
        ),
        F.text.lower().in_({
            'кто я',
            'профиль',
            'id',
            'мой id',
            'ид',
        }),
    ),
    StateFilter('*'),
)
async def on_show_profile(
        message: Message,
        user_repository: UserRepository,
) -> None:
    if message.reply_to_message is None:
        from_user = message.from_user
    else:
        from_user = message.reply_to_message.from_user

    user = await user_repository.get_by_id(from_user.id)

    if user.id == 6209548376:
        photo = URLInputFile('https://i.imgur.com/VPg0Op4.jpeg')
    elif user.profile_photo_url is not None:
        photo = URLInputFile(str(user.profile_photo_url))
    else:
        profile_photos = await from_user.get_profile_photos()
        if profile_photos.photos:
            photo = profile_photos.photos[0][-1].file_id
        else:
            url = (
                'https://api.thecatapi.com/v1/'
                'images/search?format=src&mime_types=jpg,png'
            )
            photo = URLInputFile(url)

    view = ProfileView(user, photo)

    await answer_photo_view(message=message, view=view)
