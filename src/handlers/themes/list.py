from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from repositories.themes import ThemeRepository
from views import ThemeListView, edit_message_by_view

__all__ = ('register_handlers',)


async def on_show_themes_list(
        callback_query: CallbackQuery,
        state: FSMContext,
        theme_repository: ThemeRepository,
) -> None:
    await state.clear()
    themes = await theme_repository.get_all()
    view = ThemeListView(themes)
    await edit_message_by_view(message=callback_query.message, view=view)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_show_themes_list,
        F.data == 'show-themes-list',
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
