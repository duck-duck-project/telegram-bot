from typing import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import Contact
from services.filters import filter_not_hidden
from views import View

__all__ = ('ContactListChooseView',)


class ContactListChooseView(View):

    def __init__(self, contacts: Iterable[Contact]):
        self.__contacts = tuple(contacts)

    def get_text(self) -> str:
        return (
            'Список ваших контактов 👱‍♂️'
            if self.__contacts else 'У вас нет контактов 😔'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        for contact in filter_not_hidden(self.__contacts):
            keyboard.row(
                InlineKeyboardButton(
                    text=contact.private_name,
                    callback_data=str(contact.id),
                ),
            )

        return keyboard.as_markup()
