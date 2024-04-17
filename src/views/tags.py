from collections.abc import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, User

from callback_data import TagDeleteCallbackData
from enums import TagWeight
from models import Tag
from services.text import int_gaps
from services.tags import TAG_WEIGHT_TO_PRICE
from views import View

__all__ = ('TagGivenView', 'TagListView', 'TagDetailView')

TAG_WEIGHT_TO_EMOJI = {
    TagWeight.GOLD: '🥇',
    TagWeight.SILVER: '🥈',
    TagWeight.BRONZE: '🥉',
}


class TagGivenView(View):

    def __init__(self, to_user: User):
        self.__to_user = to_user

    def get_text(self) -> str:
        return f'✅ Награда выдана пользователю {self.__to_user.mention_html()}'


class TagListView(View):

    def __init__(self, user: User, tags: Iterable[Tag]):
        self.__tags = tuple(tags)
        self.__user = user

    def get_text(self) -> str:
        if not self.__tags:
            return f'🏆 У {self.__user.mention_html()} нет наград'

        lines: list[str] = [f'<b>🏆 Награды {self.__user.mention_html()}:</b>']

        for tag_number, tag in enumerate(self.__tags, start=1):
            emoji = TAG_WEIGHT_TO_EMOJI[tag.weight]
            lines.append(
                f'{tag_number}. {emoji} {tag.text}'
            )

        total_price = sum(
            TAG_WEIGHT_TO_PRICE[tag.weight] for tag in self.__tags
        )
        lines.append(
            f'<b>💰  Общая стоимость {int_gaps(total_price)} дак-дак коинов</b>'
        )

        lines.append(
            '\n❓ Чтобы лучше рассмотреть награду, используйте команду:\n'
            '<code>награда {номер награды}</code>'
        )

        return '\n'.join(lines)


class TagDetailView(View):

    def __init__(self, tag: Tag, to_user: User):
        self.__tag = tag
        self.__to_user = to_user

    def get_text(self) -> str:
        from_user = self.__tag.of_user_username or self.__tag.of_user_fullname
        emoji = TAG_WEIGHT_TO_EMOJI[self.__tag.weight]
        return (
            f'🏆 <b>Награда для {self.__to_user.mention_html()}</b>\n'
            f'От: {from_user}\n'
            f'Текст: {self.__tag.text}\n'
            f'{emoji} Статус: {self.__tag.weight.name.lower()}\n'
            f'Выдана {self.__tag.created_at:%d.%m.%Y %H:%M} (UTC)'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        button = InlineKeyboardButton(
            text='💰 Продать',
            callback_data=TagDeleteCallbackData(
                tag_id=self.__tag.id,
                tag_weight=self.__tag.weight,
            ).pack(),
        )
        return InlineKeyboardMarkup(inline_keyboard=[[button]])
