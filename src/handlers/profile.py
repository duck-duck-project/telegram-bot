from aiogram import F, Router
from aiogram.filters import StateFilter, and_f, or_f
from aiogram.types import Message

from repositories import UserRepository
from services import get_user_profile_photo
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

    photo = await get_user_profile_photo(
        user=from_user,
        profile_photo_url=user.profile_photo_url,
    )

    view = ProfileView(user, photo)

    await answer_photo_view(message=message, view=view)
