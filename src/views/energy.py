from collections.abc import Iterable
from typing import assert_never

from enums import FoodType
from models import FoodItem, UserEnergyRefill
from services.food import render_energy
from views import View

__all__ = ('EnergyRefillView', 'FoodItemsListView')


class EnergyRefillView(View):

    def __init__(
            self,
            food_item: FoodItem,
            user_energy_refill: UserEnergyRefill,
    ):
        self.__food_item = food_item
        self.__user_energy_refill = user_energy_refill

    def get_text(self) -> str:
        if self.__food_item.type == FoodType.DRINK:
            text = f'{self.__food_item.emoji} Вы выпили <b>{self.__food_item.name}</b>\n'
        elif self.__food_item.type == FoodType.FOOD:
            text = f'{self.__food_item.emoji} Вы съели <b>{self.__food_item.name}</b>\n'
        else:
            assert_never(self.__food_item.type)
        text += (
            f'✅ Восстановлено {render_energy(self.__food_item.energy)} энергии\n'
            f'🔋 Ваша энергия: {render_energy(self.__user_energy_refill.energy)}'
        )
        return text


class FoodItemsListView(View):

    def __init__(self, food_items: Iterable[FoodItem]):
        self.__food_items = tuple(food_items)

    def get_text(self) -> str:
        foods = [
            (f'{food.emoji} <b>{food.name}</b> - {food.price}'
             f' - {render_energy(food.energy)}')
            for food in self.__food_items
            if food.type == FoodType.FOOD
        ]
        drinks = [
            (f'{drink.emoji} <b>{drink.name}</b> - {drink.price}'
             f' - {render_energy(drink.energy)}')
            for drink in self.__food_items
            if drink.type == FoodType.DRINK
        ]
        lines: list[str] = []

        if foods:
            lines.append('🍔 Еда (цена, энергия):')
            lines.extend(foods)

        lines.append('')

        if drinks:
            lines.append('🥤 Напитки (цена, энергия):')
            lines.extend(drinks)

        return '\n'.join(lines)
