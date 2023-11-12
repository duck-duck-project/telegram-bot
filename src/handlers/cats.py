import random

from aiogram import Router, F
from aiogram.filters import StateFilter, Command, or_f
from aiogram.types import Message, URLInputFile

from repositories import BalanceRepository
from services import BalanceNotifier

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    or_f(
        Command('meow'),
        F.text == '🐾 Котик',
    ),
    StateFilter('*'),
)
async def on_send_cat_photo(
        message: Message,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    url = (
        'https://api.thecatapi.com/v1/images/search?'
        'format=src&mime_types=jpg,png'
    )
    withdrawal = await balance_repository.create_withdrawal(
        user_id=message.from_user.id,
        amount=100,
        description='🐱 Фото котика',
    )
    await message.reply_photo(URLInputFile(url))
    await balance_notifier.send_withdrawal_notification(withdrawal)
