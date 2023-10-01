from aiogram import Router
from aiogram.filters import StateFilter, Command, ExceptionTypeFilter
from aiogram.types import Message, ErrorEvent

from exceptions import InsufficientFundsForBetError
from filters import (
    bet_on_even_or_odd_number_filter,
    bet_on_specific_number_filter,
    bet_on_specific_color_filter,
    bet_amount_filter,
)
from models import BetColor, User, BetEvenOrOdd
from repositories import BalanceRepository
from services import (
    BalanceNotifier,
    get_roulette_with_random_number,
    process_roulette_won,
    process_roulette_failed,
    validate_user_balance,
)
from views import CasinoFAQView, reply_view

router = Router(name=__name__)

__all__ = ('router',)


@router.error(ExceptionTypeFilter(InsufficientFundsForBetError))
async def on_insufficient_funds_for_bet_error(event: ErrorEvent) -> None:
    await event.update.message.reply('❌ У вас недостаточно средств для ставки')


@router.message(
    Command('bet'),
    bet_on_specific_color_filter,
    bet_amount_filter,
    StateFilter('*'),
)
async def on_make_bet_on_specific_color(
        message: Message,
        target_color: BetColor,
        bet_amount: int,
        balance_repository: BalanceRepository,
        user: User,
        balance_notifier: BalanceNotifier,
) -> None:
    roulette = get_roulette_with_random_number()

    await validate_user_balance(
        balance_repository=balance_repository,
        user_id=user.id,
        bet_amount=bet_amount,
    )

    if target_color == BetColor.GREEN and roulette.is_zero():
        await message.reply('Вам выпало число 0, ваша ставка возвращается вам')

    if target_color == roulette.determine_color():
        await process_roulette_won(
            roulette=roulette,
            bet_amount=int(bet_amount * 0.9),
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )
    else:
        await process_roulette_failed(
            roulette=roulette,
            bet_amount=bet_amount,
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )


@router.message(
    Command('bet'),
    bet_on_specific_number_filter,
    bet_amount_filter,
    StateFilter('*'),
)
async def on_make_bet_on_specific_number(
        message: Message,
        target_number: int,
        bet_amount: int,
        balance_repository: BalanceRepository,
        user: User,
        balance_notifier: BalanceNotifier,
) -> None:
    roulette = get_roulette_with_random_number()

    await validate_user_balance(
        balance_repository=balance_repository,
        user_id=user.id,
        bet_amount=bet_amount,
    )

    if target_number == roulette.number and roulette.is_zero():
        await message.reply('Вам выпало число 0, ваша ставка возвращается вам')
        return

    if target_number == roulette.number:
        await process_roulette_won(
            roulette=roulette,
            bet_amount=bet_amount * 36,
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )
    else:
        await process_roulette_failed(
            roulette=roulette,
            bet_amount=bet_amount,
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )


@router.message(
    Command('bet'),
    bet_on_even_or_odd_number_filter,
    bet_amount_filter,
    StateFilter('*'),
)
async def on_make_bet_on_even_or_odd_number(
        message: Message,
        target_even_or_odd: BetEvenOrOdd,
        bet_amount: int,
        balance_repository: BalanceRepository,
        user: User,
        balance_notifier: BalanceNotifier,
) -> None:
    roulette = get_roulette_with_random_number()

    await validate_user_balance(
        balance_repository=balance_repository,
        user_id=user.id,
        bet_amount=bet_amount,
    )

    result_even_or_odd = roulette.determine_even_or_odd()
    if result_even_or_odd == target_even_or_odd and roulette.is_zero():
        await message.reply('Вам выпало число 0, ваша ставка возвращается вам')
        return

    if target_even_or_odd == roulette.determine_even_or_odd():
        await process_roulette_won(
            roulette=roulette,
            bet_amount=int(bet_amount * 0.9),
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )
    else:
        await process_roulette_failed(
            roulette=roulette,
            bet_amount=bet_amount,
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )


@router.message(
    Command('bet'),
    StateFilter('*'),
)
async def on_bet(message: Message) -> None:
    await reply_view(view=CasinoFAQView(), message=message)
