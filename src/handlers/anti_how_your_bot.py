from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from exceptions import InsufficientFundsForWithdrawalError
from repositories import BalanceRepository
from services import BalanceNotifier, try_to_delete_message

router = Router(name=__name__)


@router.message(
    F.via_bot.username == 'HowYourBot',
    StateFilter('*'),
)
async def on_how_your_bot_message(
        message: Message,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    price = 100
    user_id = message.from_user.id
    try:
        withdrawal = await balance_repository.create_withdrawal(
            user_id=user_id,
            amount=price,
            description='Использование @HowYourBot',
        )
    except InsufficientFundsForWithdrawalError:
        if message.from_user.username is None:
            link = f'tg://openmessage?user_id={message.from_user.id}'
        else:
            link = f'https://t.me/{message.from_user.username}'
        await message.answer(
            f'❗️ <a href="{link}">{message.from_user.full_name}</a>'
            ' пополните баланс чтобы использовать @HowYourBot.'
            '\n💰 Узнать свой баланс /balance',
            disable_web_page_preview=True,
        )
        await try_to_delete_message(message)
    else:
        await balance_notifier.send_withdrawal_notification(withdrawal)
