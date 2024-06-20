from collections.abc import Iterable

from enums import FoodItemType
from models import FoodItem

__all__ = (
    'filter_junk_food_items',
    'filter_healthy_food_items',
    'filter_by_food_item_type',
)


def filter_by_food_item_type(
        items: Iterable[FoodItem],
        food_item_type: FoodItemType,
) -> list[FoodItem]:
    return [item for item in items if item.type == food_item_type]


def filter_healthy_food_items(items: Iterable[FoodItem]) -> list[FoodItem]:
    return [item for item in items if item.health_impact_value >= 0]


def filter_junk_food_items(items: Iterable[FoodItem]) -> list[FoodItem]:
    return [item for item in items if item.health_impact_value < 0]
