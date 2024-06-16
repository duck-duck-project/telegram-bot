from aiogram.types import Message

from enums import FoodType
from services.food import FoodItems

__all__ = ('commands_to_food_type', 'energy_refill_filter')

commands_to_food_type = {
    ('покушать', 'поесть'): FoodType.FOOD,
    ('попить',): FoodType.DRINK,
}


def energy_refill_filter(
        message: Message,
        food_items: FoodItems,
) -> dict | bool:
    if message.text is None:
        return False

    try:
        command_input, food_item_name = message.text.split(' ', maxsplit=1)
    except ValueError:
        return False

    food_type: FoodType | None = None
    for commands in commands_to_food_type:
        for command in commands:
            if command == command_input.lower():
                food_type = commands_to_food_type[commands]

    if food_type is None:
        return False

    food_item = food_items.find_by_name(
        name=food_item_name,
        food_type=food_type,
    )
    if food_item is None:
        return False

    return {'food_item': food_item}
