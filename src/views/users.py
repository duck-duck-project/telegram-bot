from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    ReplyKeyboardMarkup,
)

from models import User
from views import InlineQueryView, View

__all__ = (
    'UserMenuView',
    'UserBannedInlineQueryView',
    'UserPersonalSettingsView',
)


class UserPersonalSettingsView(View):
    text = 'Настройки профиля'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='🏞️ Фото профиля',
                        callback_data='update-profile-photo',
                    )
                ]
            ],
        )


class UserMenuView(View):
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='📩 Секретное сообщение'),
                KeyboardButton(text='🖼️ Секретное медиа'),
            ],
            [
                KeyboardButton(text='💰 Финансы'),
                KeyboardButton(text='🍽️ Йемек'),
            ],
            [
                KeyboardButton(text='🐾 Котик'),
                KeyboardButton(text='🐶 Собачка'),
            ],
            [
                KeyboardButton(text='🎨 Настройки'),
            ],
        ],
    )

    def __init__(
            self,
            user: User,
            is_anonymous_messaging_enabled: bool,
            balance: int,
    ):
        self.__user = user
        self.__is_anonymous_messaging_enabled = is_anonymous_messaging_enabled
        self.__balance = balance

    def get_text(self) -> str:
        name = self.__user.username_or_fullname
        if self.__user.profile_photo_url is not None:
            name = f'<a href="{self.__user.profile_photo_url}">{name}</a>'
        return (
            f'🙎🏿‍♂️ Имя: {name}\n'
            f'💰 Баланс: 🐥${self.__balance}\n'
        )


class UserBannedInlineQueryView(InlineQueryView):
    title = 'Вы заблокированы в боте 😔'
    description = 'Обратитесь к @usbtypec для разблокировки'
    text = 'Я заблокирован в боте и не могу его использовать 😔'
    thumbnail_url = 'https://i.imgur.com/JGgzhAI.jpg'
    thumbnail_height = 100
    thumbnail_width = 100
