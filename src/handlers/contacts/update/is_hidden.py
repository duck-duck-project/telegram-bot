from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message

from callback_data import ContactUpdateCallbackData
from repositories import ContactRepository
from views import edit_message_by_view, ContactDetailView

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    Command('hide', 'show'),
    F.reply_to_message.as_('reply_to_message'),
    StateFilter('*'),
)
async def on_toggle_is_hidden_status_command(
        message: Message,
        reply_to_message: Message,
        contact_repository: ContactRepository,
) -> None:
    is_hidden = message.text.startswith('/hide')

    contacts = await contact_repository.get_by_user_id(message.from_user.id)

    contact_to_update = None
    for contact in contacts:
        if contact.to_user.id == reply_to_message.from_user.id:
            contact_to_update = contact
            break

    if contact_to_update is None:
        await message.reply(
            f'❌ {reply_to_message.from_user.full_name} не ваш контакт')
        return

    await contact_repository.update(
        contact_id=contact_to_update.id,
        public_name=contact_to_update.public_name,
        private_name=contact_to_update.private_name,
        is_hidden=is_hidden,
    )
    text = '🙈 Контакт скрыт' if is_hidden else '🙉 Контакт больше не скрыт'
    await message.reply(text)


@router.callback_query(
    ContactUpdateCallbackData.filter(F.field == 'is_hidden'),
    F.message.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
async def on_toggle_is_hidden_status(
        callback_query: CallbackQuery,
        callback_data: ContactUpdateCallbackData,
        contact_repository: ContactRepository,
) -> None:
    contact = await contact_repository.get_by_id(callback_data.contact_id)
    await contact_repository.update(
        contact_id=callback_data.contact_id,
        public_name=contact.public_name,
        private_name=contact.private_name,
        is_hidden=not contact.is_hidden,
    )
    contact = await contact_repository.get_by_id(callback_data.contact_id)

    view = ContactDetailView(contact)
    await edit_message_by_view(message=callback_query.message, view=view)
    await callback_query.answer('✅ Статус скрытости обновлен')
