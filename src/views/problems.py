from models import ArithmeticExpression
from views.base import View

__all__ = ('ArithmeticProblemView', 'ArithmeticProblemSolvedView')


class ArithmeticProblemView(View):

    def __init__(
            self,
            *,
            expression: ArithmeticExpression,
            reward: int,
            premium_multiplier: int | float,
    ):
        self.__expression = expression
        self.__reward = reward
        self.__premium_multiplier = premium_multiplier

    def get_text(self) -> str:
        return (
            f'❓ Сколько будет: {self.__expression}?\n'
            f'💰 Награда: {self.__reward} дак-дак коинов'
            f' (x{self.__premium_multiplier} для премиум пользователей 🌟)'
        )


class ArithmeticProblemSolvedView(View):

    def __init__(self, amount_to_deposit: int):
        self.__amount_to_deposit = amount_to_deposit

    def get_text(self) -> str:
        return (
            f'✅ Правильно!\n'
            f' Награда: {self.__amount_to_deposit} дак-дак коинов\n'
            '🙂 Продолжить /work'
        )
