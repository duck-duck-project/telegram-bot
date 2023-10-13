from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram.types import InputMediaPhoto

from models import DailyFoodMenu
from views.base import View

__all__ = ('FoodMenuMediaGroupView',)


class FoodMenuMediaGroupView(View):

    def __init__(self, daily_food_menu: DailyFoodMenu):
        self.__daily_food_menu = daily_food_menu

    def get_text(self) -> str:
        caption: list[str] = [
            f'🍽️ <b>Меню на {self.__daily_food_menu.at:%d.%m.%Y}</b>\n'
        ]

        total_calories_count: int = 0

        for food_menu_item in self.__daily_food_menu.items:
            caption.append(f'▻ {food_menu_item.name}')
            caption.append(f'◦ Калории: {food_menu_item.calories_count}\n')

            total_calories_count += food_menu_item.calories_count

        caption.append(f'Сумма калорий: {total_calories_count}')
        return '\n'.join(caption)

    def as_media_group(self) -> list[InputMediaPhoto]:
        first = InputMediaPhoto(
            media=str(self.__daily_food_menu.items[0].photo_url),
            caption=self.get_text(),
        )

        return [first] + [
            InputMediaPhoto(
                media=str(food_menu_item.photo_url),
            ) for food_menu_item in self.__daily_food_menu.items[1:]
        ]
