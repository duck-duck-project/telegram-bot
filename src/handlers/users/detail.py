from aiogram import Bot, F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.profile import on_show_profile
from repositories import UserRepository
from views import UserMenuView, UserSettingsCalledInGroupChatView, answer_view

__all__ = ('register_handlers',)


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
