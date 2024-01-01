from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from repositories import ContactRepository
from views import render_message_or_callback_query, ContactListView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    F.data == 'show-contacts-list',
    F.message.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
@router.message(
    F.text == '👥 Контакты',
    F.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
async def on_show_contacts_list(
        message_or_callback_query: Message | CallbackQuery,
        contact_repository: ContactRepository,
        state: FSMContext,
) -> None:
    await state.clear()
    user_id = message_or_callback_query.from_user.id
    contacts = await contact_repository.get_by_user_id(user_id)
    view = ContactListView(contacts)
    await render_message_or_callback_query(
        message_or_callback_query=message_or_callback_query,
        view=view,
    )
