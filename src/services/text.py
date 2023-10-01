__all__ = ('int_gaps',)


def int_gaps(number: str) -> str:
    return f'{number:_}'.replace('_', ' ')
