from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.types import Message

from filters import (
    bet_on_even_or_odd_number_filter,
    bet_on_specific_number_filter,
    bet_on_specific_color_filter,
    bet_amount_filter,
)
from models import BetColor, User, BetEvenOrOdd
from repositories import BalanceRepository
from services import BalanceNotifier
from services.casino import get_roulette_with_random_number

router = Router(name=__name__)

__all__ = ('router',)


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

    user_balance = await balance_repository.get_user_balance(user.id)

    if user_balance.balance < bet_amount:
        await message.reply('У вас недостаточно средств для ставки')
        return

    if target_color == BetColor.GREEN and roulette.is_zero():
        await message.reply('Вам выпало число 0, ваша ставка возвращается вам')

    if target_color == roulette.determine_color():
        await message.reply('Вы выиграли!')
        deposit = await balance_repository.create_deposit(
            user_id=user.id,
            amount=bet_amount,
            description='Выигрыш в казино',
        )
        await balance_notifier.send_deposit_notification(deposit)
    else:
        await message.reply('Вы проиграли!')
        withdrawal = await balance_repository.create_withdrawal(
            user_id=user.id,
            amount=bet_amount,
            description='Проигрыш в казино',
        )
        await balance_notifier.send_withdrawal_notification(withdrawal)


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

    user_balance = await balance_repository.get_user_balance(user.id)

    if user_balance.balance < bet_amount:
        await message.reply('У вас недостаточно средств для ставки')
        return

    if target_number == roulette.number and roulette.is_zero():
        await message.reply('Вам выпало число 0, ваша ставка возвращается вам')
        return

    if target_number == roulette.number:
        await message.reply(f'Выпало число {roulette.number}. Вы выиграли!')
        deposit = await balance_repository.create_deposit(
            user_id=user.id,
            amount=bet_amount * 50,
            description='Выигрыш в казино',
        )
        await balance_notifier.send_deposit_notification(deposit)
    else:
        await message.reply(f'Выпало число {roulette.number}. Вы проиграли!')
        withdrawal = await balance_repository.create_withdrawal(
            user_id=user.id,
            amount=bet_amount,
            description='Проигрыш в казино',
        )
        await balance_notifier.send_withdrawal_notification(withdrawal)


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

    user_balance = await balance_repository.get_user_balance(user.id)

    if user_balance.balance < bet_amount:
        await message.reply('У вас недостаточно средств для ставки')
        return

    result_even_or_odd = roulette.determine_even_or_odd()
    if result_even_or_odd == target_even_or_odd and roulette.is_zero():
        await message.reply('Вам выпало число 0, ваша ставка возвращается вам')
        return

    if target_even_or_odd == roulette.determine_even_or_odd():
        await message.reply(f'Выпало число {roulette.number}. Вы выиграли!')
        deposit = await balance_repository.create_deposit(
            user_id=user.id,
            amount=bet_amount,
            description='Выигрыш в казино',
        )
        await balance_notifier.send_deposit_notification(deposit)
    else:
        await message.reply(f'Выпало число {roulette.number}. Вы проиграли!')
        withdrawal = await balance_repository.create_withdrawal(
            user_id=user.id,
            amount=bet_amount,
            description='Проигрыш в казино',
        )
        await balance_notifier.send_withdrawal_notification(withdrawal)


@router.message(
    Command('bet'),
    StateFilter('*'),
)
async def on_bet(
        message: Message,
) -> None:
    await message.reply(
        '🎲 Сделать ставку:'
        '\n\n'
        '🎨 <b>1. По цвету</b>'
        '\n'
        '<code>/bet {red или black} {сумма}</code>'
        '\n'
        'Выигрыш: 2x'
        '\n\n'
        '🔢 <b>2. На конкретное число</b>'
        '\n'
        '<code>/bet {число от 0 до 36} {сумма}</code>'
        '\n'
        'Выигрыш: 50x'
        '\n\n'
        '⚖️ <b>3. На четное или нечетное число</b>'
        '\n'
        '<code>/bet {even или odd} {сумма}</code>'
        '\n'
        'Выигрыш: 2x'
        '\n\n'
        'Сумма должна быть от 1 до 10000 дак-дак коинов'
    )
