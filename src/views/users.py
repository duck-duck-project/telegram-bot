from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

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
    text = 'Меню пользователя'
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='📩 Секретное сообщение'),
                KeyboardButton(text='🖼️ Секретное медиа'),
            ],
            [
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


class UserBannedInlineQueryView(InlineQueryView):
    title = 'Вы заблокированы в боте 😔'
    description = 'Обратитесь к @usbtypec для разблокировки'
    text = 'Я заблокирован в боте и не могу его использовать 😔'
    thumbnail_url = 'https://i.imgur.com/JGgzhAI.jpg'
    thumbnail_height = 100
    thumbnail_width = 100
