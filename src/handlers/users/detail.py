from aiogram import Bot, Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.profile import on_show_profile
from models import User
from repositories import BalanceRepository, UserRepository
from services import extract_user_from_update
from views import (
    UserSettingsCalledInGroupChatView,
    UserMenuView,
    render_message_or_callback_query,
)
from views import answer_view, edit_message_by_view, UserPersonalSettingsView

__all__ = ('register_handlers',)


async def on_show_personal_settings(
        message_or_callback_query: Message | CallbackQuery,
) -> None:
    view = UserPersonalSettingsView()
    await render_message_or_callback_query(
        message_or_callback_query=message_or_callback_query,
        view=view,
    )


async def on_settings_in_group_chat(
        message: Message,
        bot: Bot,
) -> None:
    me = await bot.get_me()
    view = UserSettingsCalledInGroupChatView(me.username)
    await answer_view(message=message, view=view)


async def on_show_settings(
        message: Message,
        state: FSMContext,
        user_repository: UserRepository,
) -> None:
    await state.clear()
    view = UserMenuView()
    await answer_view(message=message, view=view)
    await on_show_profile(message=message, user_repository=user_repository)


def register_handlers(router: Router) -> None:
    router.message.register(
        on_show_personal_settings,
        F.text == '🎨 Настройки',
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
    router.callback_query.register(
        on_show_personal_settings,
        F.data == 'show-personal-settings',
        StateFilter('*'),
    )
    router.message.register(
        on_settings_in_group_chat,
        Command('settings'),
        F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
        StateFilter('*'),
    )
    router.message.register(
        on_show_settings,
        F.text.in_({
            '/start',
            '/settings',
        }),
        F.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
