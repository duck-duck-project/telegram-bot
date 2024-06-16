import pathlib
from collections.abc import Iterable

from pydantic import TypeAdapter

from enums import FoodType
from models import FoodItem

__all__ = ('FoodItems', 'load_food_items', 'render_energy')


def load_food_items(file_path: pathlib.Path) -> tuple[FoodItem, ...]:
    type_adapter = TypeAdapter(tuple[FoodItem, ...])
    food_items_json = file_path.read_text(encoding='utf-8')
    return type_adapter.validate_json(food_items_json)


class FoodItems:

    def __init__(self, food_items: Iterable[FoodItem]):
        self.__food_items = tuple(food_items)

    def find_by_name(self, name: str, food_type: FoodType) -> FoodItem | None:
        for food_item in self.__food_items:
            if food_item.name.lower() == name.lower() and food_item.type == food_type:
                return food_item

    def __iter__(self):
        return iter(self.__food_items)


def render_energy(energy: int) -> str:
    return f'{energy / 100} ед.'
