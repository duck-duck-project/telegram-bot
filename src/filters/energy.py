from aiogram.types import Message

from enums import FoodItemType

__all__ = ('commands_and_food_type', 'food_item_filter')

commands_and_food_type = (
    (('покушать', 'поесть', 'съесть'), FoodItemType.FOOD),
    (('попить', 'выпить'), FoodItemType.DRINK),
)


def find_food_item_type_and_name(text: str) -> tuple[FoodItemType, str] | None:
    for commands, food_item_type in commands_and_food_type:
        for command in commands:
            if text.lower().startswith(f'{command} '):
                return food_item_type, text[len(command):].strip()


def food_item_filter(
        message: Message,
) -> dict | bool:
    if message.text is None:
        return False

    result = find_food_item_type_and_name(message.text)

    if result is None:
        return False

    food_item_type, food_item_name = result

    return {'food_item_type': food_item_type, 'food_item_name': food_item_name}
