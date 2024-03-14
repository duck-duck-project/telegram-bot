from collections.abc import Iterable
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callback_data import (
    SecretMessageDeleteCallbackData,
    SecretMessageDetailCallbackData,
)
from models import (
    Contact,
    SecretMedia,
    SecretMediaType,
    SecretMessage,
    Theme,
)
from views import CallbackQueryAnswerView, InlineQueryView, View

__all__ = (
    'SecretMessageDetailInlineQueryView',
    'SecretMessageTextMissingInlineQueryView',
    'NotPremiumUserInlineQueryView',
    'TooLongSecretMessageTextInlineQueryView',
    'NoUserContactsInlineQueryView',
    'SecretMediaCreateContactListView',
    'SecretMediaCreateConfirmView',
    'SecretMediaDetailView',
    'SecretMediaForShareView',
    'SecretMediaCalledInGroupChatView',
    'UserSettingsCalledInGroupChatView',
    'SecretMessagePromptView',
    'SecretMessageNotificationView',
    'NoVisibleContactsInlineQueryView',
    'SecretMessageDeletedConfirmationView',
    'SecretMessageReadConfirmationView',
)


class SecretMessageReadConfirmationView(View):

    def __init__(self, secret_message: SecretMessage):
        self.__secret_message = secret_message

    def get_text(self) -> str:
        theme = self.__secret_message.sender.theme
        recipient_name = self.__secret_message.recipient.username_or_fullname

        if self.__secret_message is None:
            template = '✅ Сообщение для {name} прочитано\n\n<i>{text}</i>'
        else:
            template = theme.secret_message_read_confirmation_text

        return template.format(
            name=recipient_name,
            text=self.__secret_message.text,
        )


class SecretMessageDeletedConfirmationView(CallbackQueryAnswerView):
    show_alert = True

    def __init__(self, theme: Theme | None):
        self.__theme = theme

    def get_text(self) -> str:
        if self.__theme is None:
            return '✅ Сообщение удалено'
        return self.__theme.secret_message_deleted_confirmation_text


class SecretMessageDetailInlineQueryView(InlineQueryView):
    thumbnail_width = 100
    thumbnail_height = 100

    def __init__(
            self,
            query_id: str,
            contact: Contact,
            secret_message_id: UUID,
            theme: Theme | None,
    ):
        self.__query_id = query_id
        self.__contact = contact
        self.__secret_message_id = secret_message_id
        self.__theme = theme

    def get_id(self) -> str:
        return self.__query_id

    def get_description(self) -> str:
        return self.__contact.public_name

    def get_thumbnail_url(self) -> str | None:
        if self.__contact.to_user.profile_photo_url is None:
            return
        return str(self.__contact.to_user.profile_photo_url)

    def get_title(self) -> str:
        return f'Контакт: {self.__contact.private_name}'

    def get_text(self) -> str:
        if self.__theme is None:
            template = (
                f'📩 Секретное сообщение для'
                ' <b>{name}</b>'
            )
        else:
            template = self.__theme.secret_message_template_text
        return template.format(name=self.__contact.public_name)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        if self.__theme is None:
            view_button_text = '👀 Прочитать'
            delete_button_text = '❌ Удалить'
        else:
            view_button_text = self.__theme.secret_message_view_button_text
            delete_button_text = self.__theme.secret_message_delete_button_text

        view_button = InlineKeyboardButton(
            text=view_button_text,
            callback_data=SecretMessageDetailCallbackData(
                secret_message_id=self.__secret_message_id,
            ).pack(),
        )
        delete_button = InlineKeyboardButton(
            text=delete_button_text,
            callback_data=SecretMessageDeleteCallbackData(
                secret_message_id=self.__secret_message_id,
            ).pack(),
        )

        return InlineKeyboardMarkup(
            inline_keyboard=[[view_button], [delete_button]]
        )


class SecretMessageTextMissingInlineQueryView(InlineQueryView):
    title = 'Введите любой текст, который хотите отправить секретно'
    text = (
        'Я чайник 🫖\n'
        'Пойду изучать <a href="https://graph.org/Kak-otpravit'
        '-sekretnoe-soobshchenie-08-14">инструкцию</a>'
    )
    thumbnail_url = 'https://i.imgur.com/e48C5cw.jpg'
    thumbnail_width = 100
    thumbnail_height = 100


class NotPremiumUserInlineQueryView(InlineQueryView):
    title = '🌟 Вы не премиум юзер'
    text = (
        'Чтобы отправить инвертированное сообщение,'
        ' вы можете приобрести премиум подписку.'
        ' Стоит она всего лишь 50 сомов в месяц.'
        ' Для покупки, напишите @usbtypec'
    )
    thumbnail_url = 'https://i.imgur.com/x9ruCcZ.jpg'
    thumbnail_width = 100
    thumbnail_height = 100


class TooLongSecretMessageTextInlineQueryView(InlineQueryView):
    title = '❌ Слишком длинное сообщение'
    text = 'Я ввёл слишком длинное сообщение 😔'
    thumbnail_url = 'https://i.imgur.com/gMh8VXO.jpg'
    thumbnail_height = 100
    thumbnail_width = 100


class NoUserContactsInlineQueryView(InlineQueryView):
    title = 'У вас пока нет контактов 😔'
    text = 'У меня пока нет контактов 😔'
    thumbnail_url = 'https://i.imgur.com/SfqYvom.jpeg'
    thumbnail_height = 100
    thumbnail_width = 100


class SecretMediaCreateContactListView(View):

    def __init__(self, contacts: Iterable[Contact]):
        self.__contacts = tuple(contacts)

    def get_text(self) -> str:
        return (
            'Выберите контакт, которому хотите отправить медиа'
            if self.__contacts else 'У вас нет контактов 😔'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=contact.private_name,
                        callback_data=str(contact.id),
                    ),
                ] for contact in self.__contacts
            ],
        )


class SecretMediaCreateConfirmView(View):

    def __init__(
            self,
            *,
            contact: Contact,
            media_type: SecretMediaType,
            description: str | None,
    ):
        self.__contact = contact
        self.__media_type = media_type
        self.__description = description

    def get_text(self) -> str:
        if self.__description is None:
            description = ''
        else:
            description = f'с описанием "{self.__description}" '
        return (
            f'Вы уверены, что хотите отправить'
            f' секретное медиа для {description}{self.__contact.private_name}?'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='❌ Отменить',
                        callback_data='cancel',
                    ),
                    InlineKeyboardButton(
                        text='✅ Отправить',
                        callback_data='confirm',
                    ),
                ],
            ],
        )


class SecretMediaDetailView(View):

    def __init__(self, secret_media: SecretMedia):
        self.__secret_media = secret_media

    def get_text(self) -> str:
        sender = (
                self.__secret_media.contact.of_user.username
                or self.__secret_media.contact.of_user.fullname
        )
        description = '' if self.__secret_media.name is None else (
            f'\nОписание: "{self.__secret_media.name}"'
        )
        return (
            '🖼️ Секретное медиа для'
            f' <b>{self.__secret_media.contact.public_name}</b>\n'
            f'Отправитель: {sender}'
            f'{description}'
        )


class SecretMediaForShareView(View):

    def __init__(
            self,
            *,
            bot_username: str,
            secret_media: SecretMedia,
            theme: Theme | None,
    ):
        self.__bot_username = bot_username
        self.__secret_media = secret_media
        self.__theme = theme

    def get_text(self) -> str:
        if self.__theme is None:
            template = '🖼️ Секретное медиа для {name}'
        else:
            template = self.__theme.secret_media_template_text

        return template.format(name=self.__secret_media.contact.public_name)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        if self.__theme is None:
            button_text = '👀 Посмотреть'
        else:
            button_text = self.__theme.secret_message_view_button_text
        url = (
            f'https://t.me/{self.__bot_username}'
            f'?start=secret_media-{self.__secret_media.id.hex}'
        )
        button = InlineKeyboardButton(text=button_text, url=url)
        return InlineKeyboardMarkup(inline_keyboard=[[button]])


class SecretMediaCalledInGroupChatView(View):
    text = f'Отправить секретное медиа можно только через личку бота'

    def __init__(self, bot_username: str):
        self.__bot_username = bot_username

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        url = f'https://t.me/{self.__bot_username}?start=secret_media'
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f'🚀 Отправить секретное медиа',
                        url=url,
                    ),
                ],
            ],
        )


class UserSettingsCalledInGroupChatView(View):
    text = 'Зайти в настройки можно только в личке бота'

    def __init__(self, bot_username: str):
        self.__bot_username = bot_username

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        url = f'https://t.me/{self.__bot_username}?start=settings'
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='⚙️ Настройки профиля',
                        url=url,
                    ),
                ],
            ],
        )


class SecretMessagePromptView(View):
    text = (
        '<a href="https://graph.org/Kak-otpravit-sekretnoe-soobshchenie-'
        '08-14">Инструкция</a> по отправке секретного сообщения'
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🚀 Отправить',
                    switch_inline_query_current_chat='',
                )
            ],
        ],
    )


class SecretMessageNotificationView(View):

    def __init__(self, *, secret_message_id: UUID, sender_full_name: str):
        self.__secret_message_id = secret_message_id
        self.__sender_full_name = sender_full_name

    def get_text(self) -> str:
        return (
            f'📩 Секретное сообщение для вас'
            f' от <b>{self.__sender_full_name}</b>'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        button = InlineKeyboardButton(
            text='👀 Прочитать',
            callback_data=SecretMessageDetailCallbackData(
                secret_message_id=self.__secret_message_id,
            ).pack(),
        )
        return InlineKeyboardMarkup(inline_keyboard=[[button]])


class NoVisibleContactsInlineQueryView(InlineQueryView):
    title = '❌ Все контакты скрыты'
    description = (
        'Перейдите в настройки бота и сделайте видимыми хотя бы один контакт'
    )
    text = 'Я скрыл все мои контакты и не могу отправить секретное сообщение 🙀'
    thumbnail_url = 'https://i.imgur.com/zAHey9P.jpg'
    thumbnail_height = 100
    thumbnail_width = 100
