from aiogram.types import Message

from models import BetColor, BetEvenOrOdd
from services import parse_abbreviated_number

__all__ = (
    'bet_on_specific_number_filter',
    'bet_on_specific_color_filter',
    'bet_on_even_or_odd_number_filter',
    'bet_amount_filter',
)


def bet_amount_filter(_: Message, bet_amount: int) -> bool | int:
    return 10 <= bet_amount <= 1_000_000


def bet_on_specific_number_filter(message: Message) -> bool | dict:
    args = message.text.lower().split(' ')

    if len(args) != 3:
        return False

    _, target_number, amount = args

    try:
        target_number = int(target_number)
    except ValueError:
        return False

    if not (0 <= target_number <= 36):
        return False

    try:
        amount = parse_abbreviated_number(amount)
    except ValueError:
        return False

    return {'target_number': target_number, 'bet_amount': amount}


def bet_on_specific_color_filter(message: Message) -> bool | dict:
    args = message.text.lower().split(' ')

    if len(args) != 3:
        return False

    _, color, amount = args

    if color not in set(BetColor):
        return False

    try:
        amount = parse_abbreviated_number(amount)
    except ValueError:
        return False

    return {'target_color': BetColor(color), 'bet_amount': amount}


def bet_on_even_or_odd_number_filter(message: Message) -> bool | dict:
    args = message.text.lower().split(' ')

    if len(args) != 3:
        return False

    _, even_or_odd, amount = args

    if even_or_odd not in set(BetEvenOrOdd):
        return False

    try:
        amount = parse_abbreviated_number(amount)
    except ValueError:
        return False

    return {
        'target_even_or_odd': BetEvenOrOdd(even_or_odd),
        'bet_amount': amount,
    }
