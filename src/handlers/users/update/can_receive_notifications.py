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
    secret_message_theme_id = None
    if user.secret_message_theme is not None:
        secret_message_theme_id = user.secret_message_theme.id

    profile_photo_url = user.profile_photo_url
    if profile_photo_url is not None:
        profile_photo_url = str(profile_photo_url)

    user, _ = await user_repository.upsert(
        user_id=callback_query.from_user.id,
        fullname=callback_query.from_user.full_name,
        username=callback_query.from_user.username,
        can_be_added_to_contacts=user.can_be_added_to_contacts,
        secret_messages_theme_id=secret_message_theme_id,
        can_receive_notifications=not user.can_receive_notifications,
        profile_photo_url=profile_photo_url,
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
