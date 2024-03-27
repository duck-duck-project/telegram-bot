from aiogram import F, Router
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import Message

from views import HelpView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    or_f(
        Command('help'),
        F.text.lower().in_({'помощь', 'инструкция'}),
    ),
    StateFilter('*'),
)
async def on_show_help(message: Message) -> None:
    view = HelpView()
    await answer_view(message=message, view=view)
