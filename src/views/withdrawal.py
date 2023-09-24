from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models import SystemTransaction
from views.base import View

__all__ = ('WithdrawalNotificationView',)


class WithdrawalNotificationView(View):

    def __init__(self, withdrawal: SystemTransaction):
        self.__withdrawal = withdrawal

    def get_text(self) -> str:
        lines = [
            f'🔥 Списание на сумму {self.__withdrawal.amount} дак-дак коинов',
        ]
        if self.__withdrawal.description is not None:
            lines.append(f'ℹ <i>{self.__withdrawal.description}</i>')
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
