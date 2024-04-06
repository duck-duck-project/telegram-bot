from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from repositories import WishRepository

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower().in_({'пожелание', 'предсказание'}),
    StateFilter('*'),
)
async def on_show_wish(
        message: Message,
        wish_repository: WishRepository,
) -> None:
    wish = await wish_repository.get_random()
    if wish is None:
        await message.answer('В моей базе пока нет пожеланий 😔')
    else:
        await message.reply(wish)
