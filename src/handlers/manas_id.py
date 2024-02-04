from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter, or_f, and_f
from aiogram.types import Message, URLInputFile

from exceptions.manas_id import ManasIdDoesNotExistError
from repositories import ManasIdRepository
from views import ManasIdView, answer_media_group_view

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
async def on_show_my_manas_id(
        message: Message,
        manas_id_repository: ManasIdRepository,
) -> None:
    from_user = (
        message.from_user
        if message.reply_to_message is None
        else message.reply_to_message.from_user
    )

    try:
        manas_id = await manas_id_repository.get_manas_id_by_user_id(
            user_id=from_user.id,
        )
    except ManasIdDoesNotExistError:
        await message.reply(
            'Пользователь отсутствует в моем реестре студентов Манаса\n'
            'Пройти регистрацию https://forms.gle/ku52NNyKmqda8HSN9',
            disable_web_page_preview=True,
        )
        return

    profile_photos = await from_user.get_profile_photos()
    if not profile_photos.photos:
        url = (
            'https://api.thecatapi.com/v1/'
            'images/search?format=src&mime_types=jpg,png'
        )
        photos = [URLInputFile(url)]
    else:
        photos = [photo[-1].file_id for photo in profile_photos.photos[:10]]

    view = ManasIdView(manas_id, photos)

    try:
        await answer_media_group_view(message=message, view=view)
    except TelegramBadRequest:
        view = ManasIdView(manas_id, photos[:1])
        await answer_media_group_view(message=message, view=view)
