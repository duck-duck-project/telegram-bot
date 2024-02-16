import textwrap

from aiogram.types import (
    InputMediaPhoto,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from callback_data import FoodMenuDetailCallbackData
from models import DailyFoodMenu
from views import MediaGroupView
from views.base import View

__all__ = ('FoodMenuMediaGroupView', 'FoodMenuFAQView')


class FoodMenuMediaGroupView(MediaGroupView):

    def __init__(self, daily_food_menu: DailyFoodMenu):
        self.__daily_food_menu = daily_food_menu

    def get_caption(self) -> str:
        caption: list[str] = [
            f'🍽️ <b>Меню на {self.__daily_food_menu.at:%d.%m.%Y}</b> 🍽️\n'
        ]

        total_calories_count: int = 0

        for food_menu_item in self.__daily_food_menu.items:
            caption.append(
                f'🧂 <u>{food_menu_item.name}</u>\n'
                f'🌱 Калории: <i>{food_menu_item.calories_count}</i>\n'
            )

            total_calories_count += food_menu_item.calories_count

        caption.append(f'<b>Сумма калорий: {total_calories_count}</b>')
        return '\n'.join(caption)

    def get_medias(self) -> list[InputMediaPhoto]:
        return [
            InputMediaPhoto(
                media=str(food_menu_item.photo_url),
            ) for food_menu_item in self.__daily_food_menu.items
        ]


class FoodMenuFAQView(View):
    text = textwrap.dedent('''\
    <b>🤤Срочный просмотр меню в йемекхане:</b>

    🍏На сегодня:
    <code>/yemek today</code>
    
    🍏На завтра:
    <code>/yemek tomorrow</code>
    
    <b>🧐Так же можно просматривать на N дней вперёд:</b>
    
    •<code>/yemek {N}</code>
    
    Например👇
    🍎На послезавтра - <code>/yemek 2</code>
    🍎10 дней вперёд - <code>/yemek 10</code>
    
    <b>👇 Так же можете посмотреть меню в онлайн режиме:</b>
    https://t.me/duck_duck_robot/yemek
    ''')
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🕕 Сегодня',
                    callback_data=FoodMenuDetailCallbackData(
                        days_skip_count=0,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text='🕒 Завтра',
                    callback_data=FoodMenuDetailCallbackData(
                        days_skip_count=1,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='🕞 Послезавтра',
                    callback_data=FoodMenuDetailCallbackData(
                        days_skip_count=2,
                    ).pack(),
                ),
            ],
        ],
    )
