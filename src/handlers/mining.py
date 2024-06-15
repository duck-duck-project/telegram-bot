from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message

from exceptions.mining import MiningActionThrottlingError
from repositories import MiningRepository
from views import (
    MinedResourceView,
    MiningActionThrottledView,
    MiningStatisticsView,
    reply_view,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(MiningActionThrottlingError))
async def on_mining_action_throttled_error(event: ErrorEvent) -> None:
    view = MiningActionThrottledView(event.exception.next_mining_in_seconds)
    await reply_view(message=event.update.message, view=view)


@router.message(
    F.text.lower().in_({'шахта', 'копать'}),
    StateFilter('*'),
)
async def on_mining(
        message: Message,
        mining_repository: MiningRepository,
) -> None:
    user_id = message.from_user.id
    mined_resource = await mining_repository.mine(user_id)
    view = MinedResourceView(mined_resource)
    await reply_view(message=message, view=view)


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
