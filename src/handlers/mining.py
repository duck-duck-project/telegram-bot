from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import Message

from exceptions.mining import MiningCooldownError
from repositories import MiningRepository
from services import get_chat_id_if_group_chat
from services.clean_up import CleanUpService
from services.mining import get_mined_resource_view
from views import (
    MiningActionThrottledView,
    MiningChatStatisticsView, MiningUserStatisticsView,
    reply_view,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower().in_({'шахта', 'копать'}),
    StateFilter('*'),
)
async def on_mining(
        message: Message,
        mining_repository: MiningRepository,
        clean_up_service: CleanUpService,
) -> None:
    user_id = message.from_user.id
    chat_id = get_chat_id_if_group_chat(message.chat)
    try:
        mined_resource = await mining_repository.mine(
            user_id=user_id,
            chat_id=chat_id,
        )
    except MiningCooldownError as error:
        view = MiningActionThrottledView(error.next_mining_in_seconds)
    else:
        view = get_mined_resource_view(mined_resource)
    sent_message = await reply_view(message=message, view=view)
    await clean_up_service.create_clean_up_task(message, sent_message)


@router.message(
    F.text.lower().in_({
        'шахта стата моя',
        'шахта статистика моя',
        'шахта моя стата',
        'шахта моя статитика',
    }),
    StateFilter('*'),
)
async def on_mining_statistics(
        message: Message,
        mining_repository: MiningRepository,
):
    user_id = message.from_user.id
    mining_statistics = await mining_repository.get_user_statistics(user_id)
    view = MiningUserStatisticsView(mining_statistics)
    await reply_view(message=message, view=view)


@router.message(
    F.text.lower().in_({
        'шахта стата чат',
        'шахта статистика чат',
        'шахта чат стата',
        'шахта чат статитика',
    }),
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    StateFilter('*'),
)
async def on_show_chat_mining_statistics(
        message: Message,
        mining_repository: MiningRepository,
):
    chat_id = message.chat.id
    mining_statistics = await mining_repository.get_chat_statistics(chat_id)
    view = MiningChatStatisticsView(mining_statistics)
    await reply_view(message=message, view=view)


@router.message(
    F.text.lower().in_({
        'шахта стата чат',
        'шахта статистика чат',
        'шахта чат стата',
        'шахта чат статитика',
    }),
    F.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
async def on_show_chat_mining_statistics_in_private_chat(message: Message):
    await message.answer('❌ Эта команда доступна только в групповых чатах')
