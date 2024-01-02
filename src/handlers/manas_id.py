from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from exceptions.manas_id import ManasIdDoesNotExistError
from repositories import ManasIdRepository
from views import ManasIdView, answer_view

router = Router(name=__name__)


@router.message(
    F.text.lower() == 'кто ты',
    F.reply_to_message.as_('reply_to_message'),
    StateFilter('*'),
)
async def on_show_other_user_manas_id(
        message: Message,
        manas_id_repository: ManasIdRepository,
        reply_to_message: Message,
) -> None:
    user_id = reply_to_message.from_user.id
    try:
        manas_id = await manas_id_repository.get_manas_id_by_user_id(user_id)
    except ManasIdDoesNotExistError:
        await message.reply(
            'Пользователь отсутствует в моем реестре студентов Манаса\n'
            'Пройти регистрацию https://forms.gle/ku52NNyKmqda8HSN9',
            disable_web_page_preview=True,
        )
        return
    view = ManasIdView(manas_id)
    await answer_view(message=message, view=view)


@router.message(
    F.text.lower() == 'кто я',
    StateFilter('*'),
)
async def on_show_my_manas_id(
        message: Message,
        manas_id_repository: ManasIdRepository,
) -> None:
    user_id = message.from_user.id
    try:
        manas_id = await manas_id_repository.get_manas_id_by_user_id(user_id)
    except ManasIdDoesNotExistError:
        await message.reply(
            'Пользователь отсутствует в моем реестре студентов Манаса\n'
            'Пройти регистрацию https://forms.gle/ku52NNyKmqda8HSN9',
            disable_web_page_preview=True,
        )
        return
    view = ManasIdView(manas_id)
    await answer_view(message=message, view=view)
