from typing import Protocol

__all__ = (
    'int_gaps',
    'parse_abbreviated_number',
    'render_grams',
    'render_units',
    'format_name_with_emoji',
)


class HasNameAndOptionalEmoji(Protocol):
    name: str
    emoji: str | None


def int_gaps(number: str | int) -> str:
    return f'{number:_}'.replace('_', ' ')


def parse_abbreviated_number(number: str) -> int:
    if not number:
        raise ValueError('Number is empty')

    if not number[0].isdigit():
        raise ValueError('Number does not start with a digit')

    abbreviations_and_values = (
        ('k', '000'),
        ('к', '000'),
    )
    for abbreviation, value in abbreviations_and_values:
        if abbreviation in number:
            number = number.replace(abbreviation, value)

    return int(number)


def render_grams(grams: int) -> str:
    if grams < 1000:
        return f'{grams} г.'

    kilograms = grams / 1000
    return f'{kilograms} кг.'


def render_units(units: int, decimal_points_shift: int = 2) -> str:
    result = str(units / 10 ** decimal_points_shift)
    integer, fraction = result.split('.')
    if fraction == '0':
        return f'{integer} ед.'
    fraction = fraction[:decimal_points_shift]
    return f'{integer},{fraction} ед.'


def format_name_with_emoji(item: HasNameAndOptionalEmoji) -> str:
    if item.emoji is not None:
        return f'{item.emoji} {item.name}'
    return item.name
