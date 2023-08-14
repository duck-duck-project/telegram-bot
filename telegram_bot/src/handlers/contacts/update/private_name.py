from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType

from callback_data import ContactUpdateCallbackData
from repositories import ContactRepository
from repositories import HTTPClientFactory
from states import ContactUpdateStates
from views import ContactDetailView
from views import answer_view

__all__ = ('register_handlers',)


async def on_start_contact_private_name_update_flow(
        callback_query: CallbackQuery,
        callback_data: dict,
        state: FSMContext,
) -> None:
    contact_id: int = callback_data['contact_id']
    await ContactUpdateStates.private_name.set()
    await state.update_data(contact_id=contact_id)
    await callback_query.message.reply(
        '🔒 Введите новое приватное имя контакта'
    )


async def on_contact_new_private_name_input(
        message: Message,
        state: FSMContext,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    state_data = await state.get_data()
    await state.finish()
    contact_id: int = state_data['contact_id']

    async with closing_http_client_factory() as http_client:
        contact_repository = ContactRepository(http_client)
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


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_contact_new_private_name_input,
        chat_type=ChatType.PRIVATE,
        state=ContactUpdateStates.private_name,
    )
    dispatcher.register_callback_query_handler(
        on_start_contact_private_name_update_flow,
        ContactUpdateCallbackData().filter(field='private_name'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )