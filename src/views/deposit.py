from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models import SystemTransaction
from views.base import View

__all__ = ('DepositNotificationView',)


class DepositNotificationView(View):

    def __init__(self, deposit: SystemTransaction):
        self.__deposit = deposit

    def get_text(self) -> str:
        lines = [
            f'✅ Пополнение на сумму {self.__deposit.amount} дак-дак коинов',
        ]
        if self.__deposit.description is not None:
            lines.append(f'ℹ <i>{self.__deposit.description}</i>')
        return '\n'.join(lines)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='💰 Мой баланс',
                        callback_data='show-user-balance',
                    ),
                ],
            ],
        )
