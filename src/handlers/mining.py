from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from exceptions.mining import MiningCooldownError
from repositories import MiningRepository
from services.clean_up import CleanUpService
from services.mining import get_mined_resource_view
from views import (
    MiningActionThrottledView,
    MiningStatisticsView,
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
    try:
        mined_resource = await mining_repository.mine(user_id)
    except MiningCooldownError as error:
        view = MiningActionThrottledView(error.next_mining_in_seconds)
    else:
        view = get_mined_resource_view(mined_resource)
    sent_message = await reply_view(message=message, view=view)
    await clean_up_service.create_clean_up_task(message, sent_message)


@router.message(
    F.text.lower().in_({'шахта стата', 'шахта статистика'}),
    StateFilter('*'),
)
async def on_mining_statistics(
        message: Message,
        mining_repository: MiningRepository,
):
    user_id = message.from_user.id
    mining_statistics = await mining_repository.get_user_statistics(user_id)
    view = MiningStatisticsView(mining_statistics)
    await reply_view(message=message, view=view)
