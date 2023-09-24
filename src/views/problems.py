from models import ArithmeticExpression
from views.base import View

__all__ = ('ArithmeticProblemView', 'ArithmeticProblemSolvedView')


class ArithmeticProblemView(View):

    def __init__(self, expression: ArithmeticExpression):
        self.__expression = expression

    def get_text(self) -> str:
        return (
            f'❓ Сколько будет: {self.__expression}?\n'
            '💰 Награда: 10 дак-дак коинов (x2 для премиум пользователей 🌟)'
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
