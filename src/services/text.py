__all__ = ('int_gaps',)


def int_gaps(number: str | int) -> str:
    return f'{number:_}'.replace('_', ' ')
