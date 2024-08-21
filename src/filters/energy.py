from aiogram.types import Message

from enums import FoodItemType

__all__ = (
    'commands_and_food_type_for_self',
    'commands_and_food_type_for_other_user',
    'feed_other_user_filter',
    'feed_self_filter',
    'find_food_item_type_and_name_for_self',
    'find_food_item_type_and_name_for_other_user',
)

commands_and_food_type_for_self = (
    (('покушать', 'поесть', 'съесть'), FoodItemType.FOOD),
    (('попить', 'выпить'), FoodItemType.DRINK),
)

commands_and_food_type_for_other_user = (
    (('покормить', 'накормить'), FoodItemType.FOOD),
    (('напоить', 'поить'), FoodItemType.DRINK),
)


def find_food_item_type_and_name_for_self(
        text: str,
) -> tuple[FoodItemType, str] | None:
    for commands, food_item_type in commands_and_food_type_for_self:
        for command in commands:
            if text.lower().startswith(f'{command} '):
                return food_item_type, text[len(command):].strip()


def find_food_item_type_and_name_for_other_user(
        text: str,
) -> tuple[FoodItemType, str] | None:
    for commands, food_item_type in commands_and_food_type_for_other_user:
        for command in commands:
            if text.lower().startswith(f'{command} '):
                return food_item_type, text[len(command):].strip()


def feed_self_filter(message: Message) -> dict | bool:
    if message.text is None:
        return False

    result = find_food_item_type_and_name_for_self(message.text)

    if result is None:
        return False

    food_item_type, food_item_name = result

    return {
        'food_item_type': food_item_type,
        'food_item_name': food_item_name,
    }


def feed_other_user_filter(message: Message) -> dict | bool:
    if message.text is None:
        return False

    if message.reply_to_message is None:
        return False

    result = find_food_item_type_and_name_for_other_user(message.text)

    if result is None:
        return False

    food_item_type, food_item_name = result

    return {
        'food_item_type': food_item_type,
        'food_item_name': food_item_name,
        'from_user': message.from_user,
        'to_user': message.reply_to_message.from_user,
    }
