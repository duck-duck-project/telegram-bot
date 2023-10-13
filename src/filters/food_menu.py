from aiogram.types import Message

__all__ = (
    'food_menu_for_n_days_filter',
    'food_menu_for_today_filter',
    'food_menu_for_tomorrow_filter',
)


def food_menu_for_today_filter(message: Message) -> bool | dict:
    if message.text.lower() != '/yemek today':
        return False
    return {'days_skip_count': 0}


def food_menu_for_tomorrow_filter(message: Message) -> bool | dict:
    if message.text.lower() != '/yemek tomorrow':
        return False
    return {'days_skip_count': 1}


def food_menu_for_n_days_filter(message: Message) -> bool | dict:
    try:
        command, days_skip_count = message.text.lower().split()
    except ValueError:
        return False
    if command != '/yemek' or not days_skip_count.isdigit():
        return False

    return {'days_skip_count': int(days_skip_count)}
