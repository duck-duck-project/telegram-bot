from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.types import Message

from repositories import BalanceRepository

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    Command('meow'),
    StateFilter('*'),
)
async def on_send_cat_photo(
        message: Message,
        balance_repository: BalanceRepository,
) -> None:
    await balance_repository.create_withdrawal(
        user_id=message.from_user.id,
        amount=100,
        description='🐱 Фото котика',
    )
    await message.reply_photo(
        photo='https://cataas.com/cat',
        caption='Вот тебе котик, держи :)',
    )
