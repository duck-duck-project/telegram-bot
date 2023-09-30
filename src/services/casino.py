import random

from models import BetColor, BetEvenOrOdd

__all__ = ('CasinoRoulette', 'get_roulette_with_random_number')


class CasinoRoulette:
    red = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
    black = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}

    def __init__(self, number: int):
        self.__number = number

    @property
    def number(self) -> int:
        return self.__number

    def is_zero(self) -> bool:
        return self.__number == 0

    def is_even(self) -> bool:
        return self.__number % 2 == 0

    def determine_even_or_odd(self) -> BetEvenOrOdd:
        return BetEvenOrOdd.EVEN if self.is_even() else BetEvenOrOdd.ODD

    def determine_color(self) -> str:
        if self.__number in self.red:
            return BetColor.RED
        elif self.__number in self.black:
            return BetColor.BLACK
        else:
            return BetColor.GREEN


def get_roulette_with_random_number() -> CasinoRoulette:
    return CasinoRoulette(random.randint(0, 36))
