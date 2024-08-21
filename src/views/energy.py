from collections.abc import Iterable

from aiogram.types import User as TelegramUser

from enums import FoodItemType
from models import FoodItem, FoodItemFeedResult
from services.food_items import (
    filter_by_food_item_type,
    filter_healthy_food_items,
    filter_junk_food_items,
)
from services.text import format_name_with_emoji, render_units
from views import View

__all__ = ('FeedSelfView', 'FoodItemsListView', 'FeedOtherUserView')


def render_action_name_for_self(food_item_type: FoodItemType) -> str:
    food_item_type_to_action_name = {
        FoodItemType.DRINK: 'выпили',
        FoodItemType.FOOD: 'съели',
    }
    return food_item_type_to_action_name.get(food_item_type, 'употребили')


def render_action_name_for_other_user(food_item_type: FoodItemType) -> str:
    food_item_type_to_action_name = {
        FoodItemType.FOOD: 'накормил',
        FoodItemType.DRINK: 'напоил',
    }
    return food_item_type_to_action_name.get(food_item_type, 'дал употребить')


def render_feed_self(
        food_item_feed_result: FoodItemFeedResult,
        food_item_type: FoodItemType,
) -> str:
    action_name = render_action_name_for_self(food_item_type)
    action = f'Вы {action_name} <b>{food_item_feed_result.food_item_name}</b>'
    if food_item_feed_result.food_item_emoji is not None:
        action = f'{food_item_feed_result.food_item_emoji} {action}'
    return action


def render_feed_other_user(
        food_item_feed_result: FoodItemFeedResult,
        food_item_type: FoodItemType,
        from_user: TelegramUser,
        to_user: TelegramUser,
) -> str:
    action_name = render_action_name_for_other_user(food_item_type)
    action = (
        f'{from_user.mention_html(from_user.username)}'
        f' {action_name}'
        f' {to_user.mention_html(to_user.username)}'
        f' блюдом: <b>{food_item_feed_result.food_item_name}</b>'
    )
    if food_item_feed_result.food_item_emoji is not None:
        action = f'{food_item_feed_result.food_item_emoji} {action}'
    return action


def render_energy(food_item_feed_result: FoodItemFeedResult) -> str:
    return (
        f'⚡️ Энергия: {render_units(food_item_feed_result.user_energy)}'
        f' (+{render_units(food_item_feed_result.energy_benefit_value)})'
    )


def render_health(
        food_item_feed_result: FoodItemFeedResult,
) -> str:
    emoji = '💚' if food_item_feed_result.health_impact_value >= 0 else '❤️'
    sign = '+' if food_item_feed_result.health_impact_value >= 0 else ''
    return (
        f'{emoji}'
        f' Здоровье: {render_units(food_item_feed_result.user_health)}'
        f' ({sign}{render_units(food_item_feed_result.health_impact_value)})'
    )


class FeedSelfView(View):

    def __init__(
            self,
            food_item_consumption_result: FoodItemFeedResult,
            food_item_type: FoodItemType,
    ):
        self.__result = food_item_consumption_result
        self.__food_item_type = food_item_type

    def get_text(self) -> str:
        lines: list[str] = [
            render_feed_self(
                food_item_feed_result=self.__result,
                food_item_type=self.__food_item_type,
            ),
            render_energy(food_item_feed_result=self.__result),
            render_health(food_item_feed_result=self.__result),
        ]
        return '\n'.join(lines)


class FeedOtherUserView(View):

    def __init__(
            self,
            food_item_consumption_result: FoodItemFeedResult,
            food_item_type: FoodItemType,
            from_user: TelegramUser,
            to_user: TelegramUser,
    ):
        self.__result = food_item_consumption_result
        self.__food_item_type = food_item_type
        self.__from_user = from_user
        self.__to_user = to_user

    def get_text(self) -> str:
        lines: list[str] = [
            render_feed_other_user(
                food_item_feed_result=self.__result,
                food_item_type=self.__food_item_type,
                from_user=self.__from_user,
                to_user=self.__to_user,
            ),
            render_energy(food_item_feed_result=self.__result),
            render_health(food_item_feed_result=self.__result),
        ]
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
            lines.append('')

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
