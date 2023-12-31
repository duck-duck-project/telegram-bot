from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import ContactDetailCallbackData
from repositories import ContactRepository
from views import edit_message_by_view, ContactDetailView

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    ContactDetailCallbackData.filter(),
    F.message.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
async def on_show_contact_detail(
        callback_query: CallbackQuery,
        callback_data: ContactDetailCallbackData,
        contact_repository: ContactRepository,
) -> None:
    contact = await contact_repository.get_by_id(callback_data.contact_id)
    view = ContactDetailView(contact)
    await edit_message_by_view(
        message=callback_query.message,
        view=view,
    )
