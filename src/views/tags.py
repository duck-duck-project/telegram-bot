from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, User

from callback_data import TagDeleteCallbackData
from enums import TagWeight
from models import UserTag, UserTags
from services.users import get_username_or_fullname
from services.tags import TAG_WEIGHT_TO_PRICE
from services.text import int_gaps
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

    def __init__(self, user_tags: UserTags):
        self.__user_tags = user_tags

    def get_text(self) -> str:
        user_name = get_username_or_fullname(self.__user_tags.user)
        if not self.__user_tags.tags:
            return f'🏆 У {user_name} нет наград'

        lines: list[str] = [f'<b>🏆 Награды {user_name}:</b>']

        for tag_number, tag in enumerate(self.__user_tags.tags, start=1):
            emoji = TAG_WEIGHT_TO_EMOJI[tag.weight]
            lines.append(f'{tag_number}. {emoji} {tag.text}')

        total_price = sum(
            TAG_WEIGHT_TO_PRICE[tag.weight] for tag in self.__user_tags.tags
        )
        lines.append(
            f'\n<b>💰  Общая стоимость {int_gaps(total_price)}'
            ' дак-дак коинов</b>'
        )

        lines.append(
            '\n❓ Чтобы лучше рассмотреть награду, используйте команду:\n'
            '<code>награда {номер награды}</code>'
        )

        return '\n'.join(lines)


class TagDetailView(View):

    def __init__(self, tag: UserTag, to_user: User):
        self.__tag = tag
        self.__to_user = to_user

    def get_text(self) -> str:
        from_user_name = get_username_or_fullname(self.__tag.of_user)
        emoji = TAG_WEIGHT_TO_EMOJI[self.__tag.weight]
        to_user_name = self.__to_user.mention_html()
        return (
            f'🏆 <b>Награда для {to_user_name}</b>\n'
            f'От: {from_user_name}\n'
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
