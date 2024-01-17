import random
from typing import Final

from aiogram.types import Message

from exceptions import InsufficientFundsForBetError
from models import BetColor, BetEvenOrOdd
from repositories import BalanceRepository
from services.notifiers import BalanceNotifier
from views import BetWonView, reply_view, BetFailedView

__all__ = (
    'CasinoRoulette',
    'get_roulette_with_random_number',
    'process_roulette_won',
    'process_roulette_failed',
    'validate_user_balance',
)


class CasinoRoulette:
    black: Final[set[int]] = {
        2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35,
    }
    red: Final[set[int]] = {
        1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36,
    }

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

    def determine_color(self) -> BetColor:
        if self.__number in self.red:
            return BetColor.RED
        elif self.__number in self.black:
            return BetColor.BLACK
        else:
            return BetColor.GREEN


def get_roulette_with_random_number() -> CasinoRoulette:
    return CasinoRoulette(random.randint(0, 36))


async def process_roulette_won(
        roulette: CasinoRoulette,
        bet_amount: int,
        message: Message,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    view = BetWonView(number=roulette.number, bet_amount=bet_amount)
    await reply_view(view=view, message=message)
    deposit = await balance_repository.create_deposit(
        user_id=message.from_user.id,
        amount=bet_amount,
        description='Выигрыш в казино',
    )
    await balance_notifier.send_deposit_notification(deposit)


async def process_roulette_failed(
        *,
        roulette: CasinoRoulette,
        bet_amount: int,
        message: Message,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    view = BetFailedView(number=roulette.number, bet_amount=bet_amount)
    await reply_view(view=view, message=message)
    withdrawal = await balance_repository.create_withdrawal(
        user_id=message.from_user.id,
        amount=bet_amount,
        description='Проигрыш в казино',
    )
    await balance_notifier.send_withdrawal_notification(withdrawal)


async def validate_user_balance(
        *,
        balance_repository: BalanceRepository,
        user_id: int,
        bet_amount: int,
) -> None:
    user_balance = await balance_repository.get_user_balance(user_id)

    if user_balance.balance < bet_amount:
        raise InsufficientFundsForBetError
