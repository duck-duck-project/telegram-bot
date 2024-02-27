from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import Message

from exceptions.manas_id import ManasIdDoesNotExistError
from exceptions.obis import ObisLoginError
from repositories import ManasIdRepository
from services.obis import login_to_obis
from views import ObisLoginView, answer_view

__all__ = ('router',)

router = Router(name=__name__)

@router.message(
    or_f(
        Command('login_obis'),
        F.text == '🚀 Войти в OBIS',
    ),
    F.chat.type != ChatType.PRIVATE,
    StateFilter('*'),
)
async def on_login_to_obis_in_group_chat(message: Message) -> None:
    await message.reply(
        '🚀 В целях безопасности,'
        ' вход в OBIS доступен только в личных сообщениях'
    )


@router.message(
    or_f(
        Command('login_obis'),
        F.text == '🚀 Войти в OBIS',
    ),
    F.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
async def on_login_to_obis(
        message: Message,
        manas_id_repository: ManasIdRepository,
) -> None:
    user_id = message.from_user.id
    try:
        manas_id = await manas_id_repository.get_manas_id_by_user_id(user_id)
    except ManasIdDoesNotExistError:
        await message.reply('У вас нет Manas ID')
        return

    if manas_id.student_id is None or manas_id.obis_password is None:
        await message.reply(
            'У вас не указан студенческий номер или пароль от OBIS\'а',
        )
        return

    try:
        login_url = await login_to_obis(
            login=manas_id.student_id,
            password=manas_id.obis_password,
        )
    except ObisLoginError as error:
        await message.reply(f'Ошибка входа в OBIS\n\n<i>{str(error)}</i>')
        return

    view = ObisLoginView(login_url)
    await answer_view(message=message, view=view)
