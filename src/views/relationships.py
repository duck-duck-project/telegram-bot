from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    User as TelegramUser,
)

from callback_data import RelationshipOfferCallbackData
from views.base import View

__all__ = ('RelationshipOfferView',)


class RelationshipOfferView(View):

    def __init__(self, from_user: TelegramUser, to_user: TelegramUser):
        self.__from_user = from_user
        self.__to_user = to_user

    def get_text(self) -> str:
        return (
            f'🌱 {self.__from_user.mention_html(self.__from_user.username)}'
            ' предложил(-а)'
            f' {self.__to_user.mention_html(self.__to_user.username)}'
            ' встречаться'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        accept_callback_data = RelationshipOfferCallbackData(
            from_user_id=self.__from_user.id,
            to_user_id=self.__to_user.id,
        ).pack()
        accept_button = InlineKeyboardButton(
            text='💚 Принять',
            callback_data=accept_callback_data,
        )
        return InlineKeyboardMarkup(inline_keyboard=[[accept_button]])
