from aiogram.types import Message

from models import BetColor, BetEvenOrOdd

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

    target_number: str
    amount: str

    if not (target_number.isdigit() and amount.isdigit()):
        return False

    target_number: int = int(target_number)

    if not (0 <= target_number <= 36):
        return False

    return {'target_number': target_number, 'bet_amount': int(amount)}


def bet_on_specific_color_filter(message: Message) -> bool | dict:
    args = message.text.lower().split(' ')

    if len(args) != 3:
        return False

    _, color, amount = args

    if color not in set(BetColor):
        return False

    return {'target_color': BetColor(color), 'bet_amount': int(amount)}


def bet_on_even_or_odd_number_filter(message: Message) -> bool | dict:
    args = message.text.lower().split(' ')

    if len(args) != 3:
        return False

    _, even_or_odd, amount = args

    if even_or_odd not in set(BetEvenOrOdd):
        return False

    return {
        'target_even_or_odd': BetEvenOrOdd(even_or_odd),
        'bet_amount': int(amount),
    }
