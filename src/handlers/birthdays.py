from zoneinfo import ZoneInfo

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from repositories import ContactRepository
from views import BirthdayListView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower().in_({'др'}),
    StateFilter('*'),
)
async def on_show_contact_birthdays(
        message: Message,
        contact_repository: ContactRepository,
        timezone: ZoneInfo,
) -> None:
    contact_birthdays = await contact_repository.get_birthdays(
        user_id=message.from_user.id,
    )
    view = BirthdayListView(contacts=contact_birthdays, timezone=timezone)
    await answer_view(message=message, view=view)
