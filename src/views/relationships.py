import random
from datetime import UTC, datetime

import humanize
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    User as TelegramUser,
)

from callback_data import RelationshipOfferCallbackData
from models import (
    Relationship,
    RelationshipBreakUpResult,
    RelationshipCreateResult,
)
from services.users import get_username_or_fullname
from views.base import View

__all__ = (
    'RelationshipOfferView',
    'RelationshipAcceptView',
    'RelationshipBreakUpConfirmationView',
    'RelationshipBreakUpResultView',
    'RelationshipDetailView',
)


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


class RelationshipAcceptView(View):

    def __init__(self, relationship_create_result: RelationshipCreateResult):
        self.__relationship_create_result = relationship_create_result

    def get_text(self) -> str:
        first_user_name = get_username_or_fullname(
            self.__relationship_create_result.first_user
        )
        second_user_name = get_username_or_fullname(
            self.__relationship_create_result.second_user
        )
        return (
            f'❤️ {first_user_name} и {second_user_name} теперь встречаются'
        )


class RelationshipBreakUpConfirmationView(View):
    choices = (
        '😔 Иногда лучше отпустить, чем продолжать страдать и тратить время в '
        'отношениях, где ты несчастен.',
        '😢 Жизнь слишком коротка, чтобы быть с кем-то, кто не делает тебя '
        'по-настоящему счастливым.',
        '😞 Может, вам обоим стоит дать друг другу шанс на новые возможности '
        'и быть с теми, кто вас ценит.',
        '😔 Оставаться в отношениях, которые больше не приносят радости, '
        'только делает больно вам обоим.',
        '😢 Иногда расставание — это первый шаг к лучшему будущему и к '
        'обретению счастья.',
        '😞 Если ты чувствуешь, что теряешь себя в этих отношениях, возможно, '
        'пора остановиться.',
        '😔 Вы оба заслуживаете быть счастливыми, но иногда для этого нужно '
        'расстаться.',
        '😢 Постоянные ссоры и недопонимания могут разрушить душевное '
        'равновесие. Может, пора остановить это?',
        '😞 Если ты чувствуешь, что больше не получаешь любви, которую '
        'заслуживаешь, возможно, пора идти дальше.',
        '😔 Боль от расставания может оказаться временной, но она даст тебе '
        'шанс начать новую, более счастливую жизнь.',
        '😢 Расставание — это большой шаг, но иногда он необходим для того, '
        'чтобы оба стали счастливее.',
    )

    def get_text(self) -> str:
        return (
            f'{random.choice(self.choices)}\n'
            'Если ты все-таки настроен серьезно, то тебе нужно ввести:\n'
            '<code>Да, я уверен и хочу расстаться</code>'
        )


class RelationshipBreakUpResultView(View):

    def __init__(self, relationship_break_up_result: RelationshipBreakUpResult):
        self.__result = relationship_break_up_result

    def get_text(self) -> str:
        duration = self.__result.broke_up_at - self.__result.created_at
        humanized_duration = humanize.precisedelta(
            duration,
            minimum_unit='minutes',
            format='%0.0f',
        )
        return (
            f'💔 {get_username_or_fullname(self.__result.first_user)} и '
            f'{get_username_or_fullname(self.__result.second_user)}'
            f' расстались\n'
            f'Их отношения продлились {humanized_duration}'
            f' и дошли до {self.__result.level}-уровня.'
        )


class RelationshipDetailView(View):

    def __init__(self, relationship: Relationship):
        self.__relationship = relationship

    def get_text(self) -> str:
        duration = datetime.now(UTC) - self.__relationship.created_at
        humanized_duration = humanize.precisedelta(
            duration,
            minimum_unit='minutes',
            format='%0.0f',
        )
        first_user_name = get_username_or_fullname(
            self.__relationship.first_user
        )
        second_user_name = get_username_or_fullname(
            self.__relationship.second_user
        )
        return (
            f'👨🏿‍❤️‍👨🏿 Отношения {first_user_name} и {second_user_name}\n'
            f'⏳ Длительность: {humanized_duration}\n'
            f'📊 {self.__relationship.level}-уровень\n'
            f'⚡️ Прогресс: {self.__relationship.experience}'
            f'/{self.__relationship.next_level_experience_threshold} XP'
        )
