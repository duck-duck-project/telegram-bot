from typing import Protocol

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from models import UserBalance, Transfer
from views.base import View

__all__ = (
    'FinanceMenuView',
    'UserBalanceView',
    'WithdrawalNotificationView',
    'DepositNotificationView',
    'TransferAskForDescriptionView',
    'TransferConfirmView',
    'TransferSuccessfullyExecutedView',
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


class FinanceMenuView(View):
    text = '📊 Финансовые операции'
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='💼 Работать'),
            ],
            [
                KeyboardButton(text='💰 Мой баланс'),
                KeyboardButton(text='💳 Перевод средств'),
            ],
            [
                KeyboardButton(text='🔙 Назад'),
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


class TransferAskForDescriptionView(View):
    text = '📝 Введите описание перевода:'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Пропустить',
                    callback_data='skip',
                ),
            ],
        ],
    )


class TransferConfirmView(View):

    def __init__(self, recipient_name, amount: int, description: str | None):
        self.__amount = amount
        self.__description = description
        self.__recipient_name = recipient_name

    def get_text(self) -> str:
        if self.__description is None:
            return (
                '❓ Вы уверены что хотите совершить перевод'
                f' на сумму в {self.__amount}'
                f' дак-дак коинов контакту {self.__recipient_name}'
            )
        return (
            '❓ Вы уверены что хотите совершить перевод'
            f' на сумму в {self.__amount}'
            f' дак-дак коинов контакту {self.__recipient_name}'
            f' с описанием <i>{self.__description}</i>'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='❌ Отменить',
                        callback_data='cancel',
                    ),
                    InlineKeyboardButton(
                        text='✅ Подтвердить',
                        callback_data='confirm',
                    ),
                ],
            ],
        )


class TransferSuccessfullyExecutedView(View):

    def __init__(self, transfer: Transfer):
        self.__transfer = transfer

    def get_text(self) -> str:
        return (
            '✅ Перевод успешно выполнен\n'
            f'💰 Сумма: {self.__transfer.amount} дак-дак коинов\n'
            f'📝 Описание: {self.__transfer.description or "отсутствует"}'
        )
