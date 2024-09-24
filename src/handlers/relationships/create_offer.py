from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import Message

from views import RelationshipOfferView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower() == 'предложить встречаться',
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    F.from_user.id == F.reply_to_message.from_user.id,
    StateFilter('*'),
)
async def on_relationship_offer_to_self(message: Message) -> None:
    await message.reply('😔 Вы не можете завести отношения с самим собой')


@router.message(
    F.text.lower() == 'предложить встречаться',
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    F.reply_to_message.from_user.is_bot,
    StateFilter('*'),
)
async def on_relationship_offer_to_bot(message: Message) -> None:
    await message.reply('😔 Вы не можете завести отношения с ботом')


@router.message(
    F.text.lower() == 'предложить встречаться',
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    F.reply_to_message,
    StateFilter('*'),
)
async def on_create_relationship_offer(message: Message) -> None:
    view = RelationshipOfferView(
        from_user=message.from_user,
        to_user=message.reply_to_message.from_user,
    )
    await answer_view(message=message, view=view)
