from aiogram.types import Message

__all__ = (
    'food_menu_for_n_days_filter',
    'food_menu_for_today_filter',
    'food_menu_for_tomorrow_filter',
)


def food_menu_for_today_filter(message: Message) -> bool | dict:
    if message.text.lower() not in (
            '/yemek today',
            'yemek today',
            'йемек сегодня',
            'йемек на сегодня',
            'еда на сегодня',
            'меню на сегодня',
    ):
        return False
    return {'days_skip_count': 0}


def food_menu_for_tomorrow_filter(message: Message) -> bool | dict:
    if message.text.lower() not in (
            '/yemek tomorrow',
            'yemek tomorrow',
            'йемек завтра',
            'йемек на завтра',
            'еда на завтра',
            'меню на завтра',
    ):
        return False
    return {'days_skip_count': 1}


def food_menu_for_n_days_filter(message: Message) -> bool | dict:
    try:
        command, days_skip_count = message.text.lower().split()
    except ValueError:
        return False

    if command not in ('/yemek', 'yemek', 'йемек'):
        return False

    if not days_skip_count.isdigit():
        return False

    return {'days_skip_count': int(days_skip_count)}
