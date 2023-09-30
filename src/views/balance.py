from typing import Protocol

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models import UserBalance
from views.base import View

__all__ = (
    'UserBalanceView',
    'WithdrawalNotificationView',
    'DepositNotificationView',
)


class HasAmountAndDescription(Protocol):
    amount: int
    description: str | None


class MyBalanceReplyKeyboardMixin:
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='💰 Мой баланс',
                    callback_data='show-user-balance',
                ),
            ],
        ],
    )


class UserBalanceView(View):

    def __init__(self, user_balance: UserBalance):
        self.__user_balance = user_balance

    def get_text(self) -> str:
        return f'💰 Баланс: {self.__user_balance.balance} дак-дак коинов'


class WithdrawalNotificationView(View, MyBalanceReplyKeyboardMixin):

    def __init__(self, withdrawal: HasAmountAndDescription):
        self.__withdrawal = withdrawal

    def get_text(self) -> str:
        lines = [
            f'🔥 Списание на сумму {self.__withdrawal.amount} дак-дак коинов',
        ]
        if self.__withdrawal.description is not None:
            lines.append(f'ℹ <i>{self.__withdrawal.description}</i>')
        return '\n'.join(lines)


class DepositNotificationView(View, MyBalanceReplyKeyboardMixin):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='💰 Мой баланс',
                    callback_data='show-user-balance',
                ),
            ],
        ],
    )

    def __init__(self, deposit: HasAmountAndDescription):
        self.__deposit = deposit

    def get_text(self) -> str:
        lines = [
            f'✅ Пополнение на сумму {self.__deposit.amount} дак-дак коинов',
        ]
        if self.__deposit.description is not None:
            lines.append(f'ℹ <i>{self.__deposit.description}</i>')
        return '\n'.join(lines)
