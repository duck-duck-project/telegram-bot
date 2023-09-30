from enum import StrEnum, auto

__all__ = ('BetColor', 'BetEvenOrOdd')


class BetColor(StrEnum):
    RED = auto()
    BLACK = auto()
    GREEN = auto()


class BetEvenOrOdd(StrEnum):
    EVEN = auto()
    ODD = auto()
