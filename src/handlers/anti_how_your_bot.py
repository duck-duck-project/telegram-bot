from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from repositories import BalanceRepository
from services import BalanceNotifier

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
    user_balance = await balance_repository.get_user_balance(user_id)
    if user_balance.balance < price:
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
        await message.delete()
    else:
        withdrawal = await balance_repository.create_withdrawal(
            user_id=user_id,
            amount=price,
            description='Использование @HowYourBot',
        )
        await balance_notifier.send_withdrawal_notification(withdrawal)
