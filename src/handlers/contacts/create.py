from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter, invert_f
from aiogram.types import CallbackQuery, Message

from callback_data import ContactCreateCallbackData
from exceptions import ContactCreateForbiddenError, ContactCreateToSelfError
from models import User
from repositories import ContactRepository, UserRepository

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    Command('contact'),
    F.reply_to_message.from_user.is_bot,
    StateFilter('*'),
)
async def on_add_bot_to_contacts(message: Message) -> None:
    await message.reply('Вы не можете добавить бота в контакты')


@router.message(
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    Command('contact'),
    F.reply_to_message.from_user.id == F.from_user.id,
    StateFilter('*'),
)
async def on_add_self_to_contacts(_: Message) -> None:
    raise ContactCreateToSelfError


@router.message(
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    Command('contact'),
    invert_f(F.reply_to_message),
    StateFilter('*'),
)
async def on_contact_command_is_not_replied_to_user(
        message: Message,
) -> None:
    await message.reply(
        'Вы должны <b><u>ответить</u></b> на сообщение другого пользователя\n'
        'Подробная инструкция: <a href="https://graph.org/Kak-dobavit'
        '-polzovatelya-v-kontakty-08-14">*ссылка*</a>'
    )


@router.message(
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    Command('contact'),
    F.reply_to_message.as_('reply_to_message'),
    StateFilter('*'),
)
async def on_add_contact(
        message: Message,
        user: User,
        user_repository: UserRepository,
        contact_repository: ContactRepository,
        reply_to_message: Message,
) -> None:
    from_user = reply_to_message.from_user
    name = from_user.username or from_user.full_name

    to_user, is_to_user_created = await user_repository.upsert(
        user_id=from_user.id,
        fullname=from_user.full_name,
        username=from_user.username,
    )

    if not to_user.can_be_added_to_contacts:
        raise ContactCreateForbiddenError

    await contact_repository.create(
        of_user_id=user.id,
        to_user_id=to_user.id,
        private_name=name,
        public_name=name,
    )
    await message.reply('✅ Контакт успешно добавлен')


@router.callback_query(
    ContactCreateCallbackData.filter(),
    StateFilter('*'),
)
async def on_create_contact_via_button_click(
        callback_query: CallbackQuery,
        callback_data: ContactCreateCallbackData,
        user_repository: UserRepository,
        contact_repository: ContactRepository,
) -> None:
    of_user_id = callback_query.from_user.id
    if callback_data.user_id == of_user_id:
        raise ContactCreateToSelfError

    to_user = await user_repository.get_by_id(callback_data.user_id)

    if not to_user.can_be_added_to_contacts:
        raise ContactCreateForbiddenError

    await contact_repository.create(
        of_user_id=of_user_id,
        to_user_id=to_user.id,
        private_name=to_user.username_or_fullname,
        public_name=to_user.username_or_fullname,
    )
    await callback_query.answer('✅ Контакт успешно добавлен', show_alert=True)
