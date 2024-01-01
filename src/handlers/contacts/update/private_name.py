from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from callback_data import ContactUpdateCallbackData
from repositories import ContactRepository
from states import ContactUpdateStates
from views import answer_view, ContactDetailView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    ContactUpdateCallbackData.filter(F.field == 'private_name'),
    F.message.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
async def on_start_contact_private_name_update_flow(
        callback_query: CallbackQuery,
        callback_data: ContactUpdateCallbackData,
        state: FSMContext,
) -> None:
    await state.set_state(ContactUpdateStates.private_name)
    await state.update_data(contact_id=callback_data.contact_id)
    await callback_query.message.reply(
        '🔒 Введите новое приватное имя контакта'
    )


@router.message(
    F.chat.type == ChatType.PRIVATE,
    StateFilter(ContactUpdateStates.private_name),
)
async def on_contact_new_private_name_input(
        message: Message,
        state: FSMContext,
        contact_repository: ContactRepository,
) -> None:
    state_data = await state.get_data()
    await state.clear()
    contact_id: int = state_data['contact_id']

    contact = await contact_repository.get_by_id(contact_id)
    await contact_repository.update(
        contact_id=contact_id,
        public_name=contact.public_name,
        private_name=message.text,
        is_hidden=contact.is_hidden,
    )
    contact = await contact_repository.get_by_id(contact_id)

    await message.reply('✅ Приватное имя контакта обновлено')
    view = ContactDetailView(contact)
    await answer_view(message=message, view=view)
