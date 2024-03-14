from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import UserUpdateCallbackData
from models import User
from repositories import UserRepository
from views import edit_message_by_view, UserPersonalSettingsView

__all__ = ('register_handlers',)


async def on_toggle_can_receive_notifications(
        callback_query: CallbackQuery,
        user_repository: UserRepository,
        user: User,
) -> None:
    user, _ = await user_repository.upsert(
        user_id=callback_query.from_user.id,
        fullname=callback_query.from_user.full_name,
        username=callback_query.from_user.username,
        can_receive_notifications=not user.can_receive_notifications,
    )
    view = UserPersonalSettingsView(user)
    await edit_message_by_view(message=callback_query.message, view=view)


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_toggle_can_receive_notifications,
        UserUpdateCallbackData.filter(F.field == 'can_receive_notifications'),
        F.message.chat.type == ChatType.PRIVATE,
        StateFilter('*'),
    )
