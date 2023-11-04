from models import HumanizedArithmeticExpression
from views.base import View

__all__ = ('ArithmeticProblemView', 'ArithmeticProblemSolvedView')


class ArithmeticProblemView(View):

    def __init__(
            self,
            *,
            expression: HumanizedArithmeticExpression,
            reward: int,
    ):
        self.__expression = expression
        self.__reward = reward

    def get_text(self) -> str:
        return (
            f'❓ Сколько будет: {self.__expression}?\n'
            f'💰 Награда: {self.__reward} дак-дак коинов'
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
