from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import (
    ContactCreateCallbackData,
    TagListCallbackData, UserBalanceDetailCallbackData,
)
from enums import Gender
from models import User
from services.dates import humanize_age
from services.food import render_energy
from services.manas_id import (
    compute_lifetime,
    determine_zodiac_sign,
    humanize_personality_type,
)
from views import PhotoView

__all__ = ('ProfileView',)


class ProfileView(PhotoView):

    def __init__(self, user: User, photo: str):
        self.__user = user
        self.__photo = photo

    def get_caption(self) -> str:
        username = self.__user.username or 'не указан'

        if (born_on := self.__user.born_on) is not None:
            age = humanize_age(born_on)
            humanized_birth_date = f'{born_on:%d.%m.%Y}'
            lifetime_in_days = compute_lifetime(born_on)
            zodiac_sign = determine_zodiac_sign(
                month=self.__user.born_on.month,
                day=self.__user.born_on.day,
            )
        else:
            age = 'не указан'
            zodiac_sign = 'не указан'
            humanized_birth_date = 'не указана'
            lifetime_in_days = 'не понятно сколько'

        gender_name = {
            Gender.MALE: 'мужской',
            Gender.FEMALE: 'женский',
            Gender.OTHER: 'другой',
        }.get(self.__user.gender, 'не указан')

        if (country := self.__user.country) is not None:
            country = f'{self.__user.country_flag_emoji} {country}'
        else:
            country = 'не указана'

        region = self.__user.region or 'не указан'
        nationality = self.__user.nationality or 'не указана'

        personality_type = humanize_personality_type(
            personality_type=self.__user.personality_type,
        )

        real_first_name = self.__user.real_first_name or 'не указано'
        real_last_name = self.__user.real_last_name or 'не указана'
        real_patronymic = self.__user.patronymic or 'не указано'

        return (
            f'<b>🪪 Пользователь:</b>\n'
            f'ID: {self.__user.id}\n'
            f'Имя: {self.__user.fullname}\n'
            f'Username: @{username}\n'
            '\n'
            '<b>📲 Личная информация:</b>\n'
            f'Имя: {real_first_name}\n'
            f'Фамилия: {real_last_name}\n'
            f'Отчество: {real_patronymic}\n'
            f'Дата рождения: {humanized_birth_date} ({age})\n'
            f'Пол: {gender_name}\n'
            f'Страна: {country}\n'
            f'Регион: {region}\n'
            f'Национальность: {nationality}\n'
            '\n'
            '<b>✏️ Прочее:</b>\n'
            f'Знак зодиака: {zodiac_sign}\n'
            f'Тип личности: {personality_type}\n'
            f'Прожил на Земле: {lifetime_in_days} дней\n'
            f'🔋 Энергия: {render_energy(self.__user.energy)}\n'
        )

    def get_photo(self) -> str:
        return self.__photo

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        balance_button = InlineKeyboardButton(
            text='💰 Баланс',
            callback_data=UserBalanceDetailCallbackData(
                user_id=self.__user.id,
            ).pack(),
        )
        tags_button = InlineKeyboardButton(
            text='🏆 Награды',
            callback_data=TagListCallbackData(
                user_id=self.__user.id,
                user_full_name=self.__user.fullname,
            ).pack()
        )
        keyboard.row(balance_button, tags_button)

        if self.__user.can_be_added_to_contacts:
            contact_button = InlineKeyboardButton(
                text='📞 Добавить в контакты',
                callback_data=ContactCreateCallbackData(
                    user_id=self.__user.id,
                ).pack(),
            )
            keyboard.row(contact_button)

        return keyboard.as_markup()
