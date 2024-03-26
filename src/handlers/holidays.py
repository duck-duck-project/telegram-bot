from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from repositories import HolidayRepository
from views import HolidayView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower().in_({
        'праздник',
        'какой сегодня праздник',
        'праздник сегодня',
    }),
    StateFilter('*'),
)
async def on_show_holiday_today(
        message: Message,
        holiday_repository: HolidayRepository,
        timezone: ZoneInfo,
) -> None:
    now = datetime.now(timezone)
    date_holidays = await holiday_repository.get_by_date(
        month=now.month,
        day=now.day,
    )
    view = HolidayView(date_holidays)
    await answer_view(message=message, view=view)
