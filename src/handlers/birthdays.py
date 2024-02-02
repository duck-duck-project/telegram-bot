from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from repositories import ManasIdRepository, BalanceRepository
from services import BalanceNotifier
from views import ClosestBirthdaysView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower().in_({
        'днюхи',
        'др',
        'birthdays',
    }),
    StateFilter('*'),
)
async def on_show_closest_birthdays(
        message: Message,
        manas_id_repository: ManasIdRepository,
        timezone: ZoneInfo,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    manas_ids = await manas_id_repository.get_all()
    withdrawal = await balance_repository.create_withdrawal(
        user_id=message.from_user.id,
        amount=10000,
        description='Просмотр ближайших дней рождений',
    )
    view = ClosestBirthdaysView(
        manas_ids=manas_ids,
        timezone=timezone,
    )
    await answer_view(message=message, view=view)
    await balance_notifier.send_withdrawal_notification(withdrawal)
