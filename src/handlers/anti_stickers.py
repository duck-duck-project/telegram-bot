from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import Message

from exceptions import InsufficientFundsForWithdrawalError
from repositories import BalanceRepository
from services import BalanceNotifier

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    F.sticker,
    StateFilter('*'),
)
async def on_sticker_in_group_chat(
        message: Message,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    try:
        withdrawal = await balance_repository.create_withdrawal(
            user_id=message.from_user.id,
            amount=100,
            description='Отправка стикера в групповом чате',
        )
    except InsufficientFundsForWithdrawalError:
        if message.from_user.username is None:
            link = f'tg://openmessage?user_id={message.from_user.id}'
        else:
            link = f'https://t.me/{message.from_user.username}'
        await message.answer(
            f'❗️ <a href="{link}">{message.from_user.full_name}</a>'
            ' пополните баланс чтобы отправить стикер'
            '\n💰 Узнать свой баланс /balance',
            disable_web_page_preview=True,
        )
        await message.delete()
    else:
        await balance_notifier.send_withdrawal_notification(withdrawal)
