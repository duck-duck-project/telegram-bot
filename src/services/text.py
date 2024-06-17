__all__ = ('int_gaps', 'parse_abbreviated_number', 'render_grams')


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
