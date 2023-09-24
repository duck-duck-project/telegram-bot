from models import UserBalance
from views.base import View

__all__ = ('UserBalanceView',)


class UserBalanceView(View):

    def __init__(self, user_balance: UserBalance):
        self.__user_balance = user_balance

    def get_text(self) -> str:
        return f'💰 Баланс: {self.__user_balance.balance} дак-дак коинов'
