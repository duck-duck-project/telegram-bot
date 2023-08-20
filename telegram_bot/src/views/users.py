from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from callback_data import UserUpdateCallbackData
from models import User
from views import View, InlineQueryView

__all__ = (
    'UserMenuView',
    'UserBannedInlineQueryView',
    'UserPersonalSettingsView',
)


class UserPersonalSettingsView(View):

    def __init__(self, user: User):
        self.__user = user

    def get_text(self) -> str:
        can_be_added_to_contacts_text = (
            '✅ Пользователи могут добавлять меня в контакты'
            if self.__user.can_be_added_to_contacts
            else '❌ Пользователям запрещено добавлять меня в контакты'
        )
        can_receive_notifications_text = (
            '🔔 Уведомления включены'
            if self.__user.can_receive_notifications
            else '🔕 Уведомления отключены'
        )
        return (
            f'{can_be_added_to_contacts_text}\n'
            f'{can_receive_notifications_text}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        can_be_added_to_contacts_toggle_button_text = (
            '❤️ Запретить добавление в контакты'
            if self.__user.can_be_added_to_contacts
            else '💚 Разрешить добавление в контакты'
        )
        can_receive_notifications_toggle_button_text = (
            '❤️ Отключить уведомления'
            if self.__user.can_receive_notifications
            else '💚 Включить уведомления'
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=can_be_added_to_contacts_toggle_button_text,
                        callback_data=UserUpdateCallbackData().new(
                            field='can_be_added_to_contacts',
                        ),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=can_receive_notifications_toggle_button_text,
                        callback_data=UserUpdateCallbackData().new(
                            field='can_receive_notifications',
                        ),
                    ),
                ],
            ],
        )


class UserMenuView(View):

    def __init__(self, user: User, is_anonymous_messaging_enabled: bool):
        self.__user = user
        self.__is_anonymous_messaging_enabled = is_anonymous_messaging_enabled

    def get_text(self) -> str:
        is_premium_emoji = '✅' if self.__user.is_premium else '❌'
        is_anonymous_messaging_enabled_emoji = (
            '✅' if self.__is_anonymous_messaging_enabled else '❌'
        )
        name = self.__user.fullname
        if self.__user.profile_photo_url is not None:
            name = f'<a href="{self.__user.profile_photo_url}">{name}</a>'
        return (
            f'🙎🏿‍♂️ Имя: {name}\n'
            f'✨ Премиум: {is_premium_emoji}\n'
            '🔒 Режим анонимных сообщений:'
            f' {is_anonymous_messaging_enabled_emoji}\n'
        )

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton('🖼️ Отправить секретное медиа'),
                    KeyboardButton('🌟 Премиум'),
                ],
                [
                    KeyboardButton('🔐 Включить анонимные сообщения'),
                ],
                [
                    KeyboardButton('🎨 Персональные настройки'),
                    KeyboardButton('👥 Мои контакты'),
                ],
            ],
        )


class UserBannedInlineQueryView(InlineQueryView):
    title = 'Вы заблокированы в боте 😔'
    description = 'Обратитесь к @usbtypec для разблокировки'
    text = 'Я заблокирован в боте и не могу его использовать 😔'
