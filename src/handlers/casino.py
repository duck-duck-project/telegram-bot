from aiogram import F, Router
from aiogram.filters import Command, ExceptionTypeFilter, StateFilter, or_f
from aiogram.types import ErrorEvent, Message
from fast_depends import Depends, inject

from exceptions import InsufficientFundsForBetError
from filters import (
    bet_amount_filter, bet_on_even_or_odd_number_filter,
    bet_on_specific_color_filter, bet_on_specific_number_filter,
)
from models import BetColor, BetEvenOrOdd, User
from repositories import BalanceRepository
from services import (
    BalanceNotifier, CasinoRoulette, get_roulette_with_random_number,
    process_roulette_failed, process_roulette_won, validate_user_balance,
)
from services.clean_up import CleanUpService
from views import CasinoFAQView, answer_photo_view

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
@inject
async def on_make_bet_on_specific_color(
        message: Message,
        target_color: BetColor,
        bet_amount: int,
        balance_repository: BalanceRepository,
        user: User,
        balance_notifier: BalanceNotifier,
        clean_up_service: CleanUpService,
        roulette: CasinoRoulette = Depends(get_roulette_with_random_number),
) -> None:
    await validate_user_balance(
        balance_repository=balance_repository,
        user_id=user.id,
        bet_amount=bet_amount,
    )

    if target_color == BetColor.GREEN and roulette.is_zero():
        await message.reply('Вам выпало число 0, ваша ставка возвращается вам')

    if target_color == roulette.determine_color():
        sent_message = await process_roulette_won(
            roulette=roulette,
            bet_amount=int(bet_amount * 0.9),
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )
    else:
        sent_message = await process_roulette_failed(
            roulette=roulette,
            bet_amount=bet_amount,
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )
    await clean_up_service.create_clean_up_task(message, sent_message)


@router.message(
    Command('bet'),
    bet_on_specific_number_filter,
    bet_amount_filter,
    StateFilter('*'),
)
@inject
async def on_make_bet_on_specific_number(
        message: Message,
        target_number: int,
        bet_amount: int,
        balance_repository: BalanceRepository,
        user: User,
        balance_notifier: BalanceNotifier,
        clean_up_service: CleanUpService,
        roulette: CasinoRoulette = Depends(get_roulette_with_random_number),
) -> None:
    await validate_user_balance(
        balance_repository=balance_repository,
        user_id=user.id,
        bet_amount=bet_amount,
    )

    if target_number == roulette.number and roulette.is_zero():
        await message.reply('Вам выпало число 0, ваша ставка возвращается вам')
        return

    if target_number == roulette.number:
        sent_message = await process_roulette_won(
            roulette=roulette,
            bet_amount=bet_amount * 36,
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )
    else:
        sent_message = await process_roulette_failed(
            roulette=roulette,
            bet_amount=bet_amount,
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )
    await clean_up_service.create_clean_up_task(message, sent_message)


@router.message(
    Command('bet'),
    bet_on_even_or_odd_number_filter,
    bet_amount_filter,
    StateFilter('*'),
)
@inject
async def on_make_bet_on_even_or_odd_number(
        message: Message,
        target_even_or_odd: BetEvenOrOdd,
        bet_amount: int,
        balance_repository: BalanceRepository,
        user: User,
        balance_notifier: BalanceNotifier,
        clean_up_service: CleanUpService,
        roulette: CasinoRoulette = Depends(get_roulette_with_random_number),
) -> None:
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
        sent_message = await process_roulette_won(
            roulette=roulette,
            bet_amount=int(bet_amount * 0.9),
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )
    else:
        sent_message = await process_roulette_failed(
            roulette=roulette,
            bet_amount=bet_amount,
            message=message,
            balance_repository=balance_repository,
            balance_notifier=balance_notifier,
        )
    await clean_up_service.create_clean_up_task(message, sent_message)


@router.message(
    or_f(
        Command('bet'),
        F.text.lower().in_({'казино', 'казиныч', 'казик', 'bet'}),
    ),
    StateFilter('*'),
)
async def on_bet(message: Message) -> None:
    await answer_photo_view(view=CasinoFAQView(), message=message)
