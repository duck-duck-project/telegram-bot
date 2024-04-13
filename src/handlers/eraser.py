from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from repositories import BalanceRepository
from services import BalanceNotifier

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.reply_to_message.as_('reply_to_message'),
    F.text.lower().in_({'стереть', 'удалить'}),
    StateFilter('*'),
)
async def on_erase_message(
        message: Message,
        reply_to_message: Message,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    withdrawal = await balance_repository.create_withdrawal(
        user_id=message.from_user.id,
        amount=100_000,
        description='Удаление сообщения'
    )
    await reply_to_message.delete()
    await message.delete()
    await balance_notifier.send_withdrawal_notification(withdrawal)
