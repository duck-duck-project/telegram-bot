from typing import Protocol

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, User

from callback_data import TransferRollbackCallbackData
from models import Transfer, UserBalance
from services.text import int_gaps
from views.base import View

__all__ = (
    'UserBalanceView',
    'WithdrawalNotificationView',
    'DepositNotificationView',
    'TransferAskForDescriptionView',
    'TransferConfirmView',
    'InsufficientFundsForSendingMediaView',
    'InsufficientFundsForHowYourBotView',
    'TransferExecutedView',
    'UserBalanceWithoutNameView',
)


class HasAmountAndDescription(Protocol):
    amount: int
    description: str | None


class UserBalanceView(View):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='💳 Купить дак-дак коины',
                    url='https://t.me/usbtypec',
                ),
            ],
        ],
    )

    def __init__(self, user_balance: UserBalance, user_fullname: str):
        self.__user_balance = user_balance
        self.__user_fullname = user_fullname

    def get_text(self) -> str:
        return (
            f'🙍🏿‍♂️ Пользователь: {self.__user_fullname}\n'
            f'💰 Баланс: {int_gaps(self.__user_balance.balance)} дак-дак коинов'
        )


class WithdrawalNotificationView(View):
    disable_notification = True

    def __init__(self, withdrawal: HasAmountAndDescription):
        self.__withdrawal = withdrawal

    def get_text(self) -> str:
        lines = [
            f'🔥 Списание на сумму'
            f' {int_gaps(self.__withdrawal.amount)} дак-дак коинов',
        ]
        if self.__withdrawal.description is not None:
            lines.append(f'ℹ <i>{self.__withdrawal.description}</i>')
        return '\n'.join(lines)


class DepositNotificationView(View):

    def __init__(self, deposit: HasAmountAndDescription):
        self.__deposit = deposit

    def get_text(self) -> str:
        lines = [
            f'✅ Пополнение на сумму'
            f' {int_gaps(self.__deposit.amount)} дак-дак коинов',
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
                f' на сумму в {int_gaps(self.__amount)}'
                f' дак-дак коинов контакту {self.__recipient_name}'
            )
        return (
            '❓ Вы уверены что хотите совершить перевод'
            f' на сумму в {int_gaps(self.__amount)}'
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


class InsufficientFundsForSendingMediaView(View):
    disable_web_page_preview = True

    def __init__(self, user: User):
        self.__user = user

    def get_text(self) -> str:
        return (
            f'❗️ <a href="{self.__user.url}">{self.__user.full_name}</a>'
            ' пополните баланс чтобы отправить стикер/GIF/видео'
            '\n💰 Узнать свой баланс /balance'
        )


class InsufficientFundsForHowYourBotView(View):
    disable_web_page_preview = True

    def __init__(self, user: User):
        self.__user = user

    def get_text(self) -> str:
        return (
            f'❗️ <a href="{self.__user.url}">{self.__user.full_name}</a>'
            ' пополните баланс чтобы использовать @HowYourBot'
            '\n💰 Узнать свой баланс /balance'
        )


class TransferExecutedView(View):

    def __init__(self, transfer: Transfer):
        self.__transfer = transfer

    def get_text(self) -> str:
        return (
            '✅ Перевод успешно выполнен\n'
            f'💰 Сумма: {int_gaps(self.__transfer.amount)} дак-дак коинов\n'
            f'📝 Описание: {self.__transfer.description or "отсутствует"}\n'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='🔙 Отменить',
                        callback_data=TransferRollbackCallbackData(
                            transfer_id=self.__transfer.id,
                        ).pack(),
                    ),
                ],
            ],
        )


class UserBalanceWithoutNameView(View):

    def __init__(self, balance: int):
        self.__balance = balance

    def get_text(self) -> str:
        return (
            f'Баланс этого пользователя:'
            f' {int_gaps(self.__balance)} дак-дак коинов'
        )
