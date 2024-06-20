from collections.abc import Iterable

from enums import FoodItemType
from models import FoodItem, FoodItemConsumptionResult
from services.text import format_name_with_emoji, render_units
from services.food_items import (
    filter_by_food_item_type,
    filter_healthy_food_items,
    filter_junk_food_items,
)
from views import View

__all__ = ('FoodItemConsumedView', 'FoodItemsListView')


class FoodItemConsumedView(View):

    def __init__(
            self,
            food_item_consumption_result: FoodItemConsumptionResult,
            food_item_type: FoodItemType,
    ):
        self.__result = food_item_consumption_result
        self.__food_item_type = food_item_type

    def get_text(self) -> str:
        food_item_type_to_action_name = {
            FoodItemType.DRINK: 'выпили',
            FoodItemType.FOOD: 'съели',
        }
        action_name = food_item_type_to_action_name.get(
            self.__food_item_type,
            'употребили',
        )
        lines: list[str] = [
            f'Вы {action_name} <b>{self.__result.food_item_name}</b>',
        ]

        if self.__result.food_item_emoji is not None:
            lines[0] = f'{self.__result.food_item_emoji} {lines[0]}'

        lines.append(
            f'⚡️ Ваша энергия: {render_units(self.__result.user_energy)}'
            f' (+{render_units(self.__result.energy_benefit_value)})'
        )

        emoji = '💚' if self.__result.health_impact_value >= 0 else '❤️'
        lines.append(
            f'{emoji} Ваше здоровье: {render_units(self.__result.user_health)}'
            f' ({render_units(self.__result.health_impact_value)})'
        )

        return '\n'.join(lines)


class FoodItemsListView(View):

    def __init__(self, food_items: Iterable[FoodItem]):
        self.__food_items = tuple(food_items)

    def get_text(self) -> str:
        healthy_food_items = filter_healthy_food_items(self.__food_items)
        healthy_foods = filter_by_food_item_type(
            items=healthy_food_items,
            food_item_type=FoodItemType.FOOD,
        )
        healthy_drinks = filter_by_food_item_type(
            items=healthy_food_items,
            food_item_type=FoodItemType.DRINK,
        )

        junk_food_items = filter_junk_food_items(self.__food_items)
        junk_foods = filter_by_food_item_type(
            items=junk_food_items,
            food_item_type=FoodItemType.FOOD,
        )
        junk_drinks = filter_by_food_item_type(
            items=junk_food_items,
            food_item_type=FoodItemType.DRINK,
        )

        lines: list[str] = []

        if healthy_foods:
            lines.append(
                '<b>🥗 Здоровая еда (цена, энергия, влияние на здоровье):</b>'
            )
            lines += [
                (f'<b>{format_name_with_emoji(food)}</b> | {food.price}'
                 f' | {render_units(food.energy_benefit_value)}'
                 f' | +{render_units(food.health_impact_value)}')
                for food in healthy_foods
            ]
            lines.append('')

        if healthy_drinks:
            lines.append(
                '<b>🥤 Здоровые напитки'
                ' (цена, энергия, влияние на здоровье):</b>'
            )
            lines += [
                (f'<b>{format_name_with_emoji(drink)}</b> | {drink.price}'
                 f' | {render_units(drink.energy_benefit_value)}'
                 f' | +{render_units(drink.health_impact_value)}')
                for drink in healthy_drinks
            ]

        if junk_foods:
            lines.append(
                '<b>🍔 Вредная еда (цена, энергия, влияние на здоровье):</b>'
            )
            lines += [
                (f'<b>{format_name_with_emoji(food)}</b> | {food.price}'
                 f' | {render_units(food.energy_benefit_value)}'
                 f' | {render_units(food.health_impact_value)}')
                for food in junk_foods
            ]
            lines.append('')

        if junk_drinks:
            lines.append(
                '<b>🥤 Вредные напитки'
                ' (цена, энергия, влияние на здоровье):</b>'
            )
            lines += [
                (f'<b>{format_name_with_emoji(drink)}</b> | {drink.price}'
                 f' | {render_units(drink.energy_benefit_value)}'
                 f' | {render_units(drink.health_impact_value)}')
                for drink in junk_drinks
            ]

        return '\n'.join(lines)
