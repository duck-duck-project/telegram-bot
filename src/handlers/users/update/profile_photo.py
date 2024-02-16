from aiogram import Router, F, Bot
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from filters import PhotoDimensionsFilter
from models import User
from repositories import UserRepository
from services import upload_photo_to_cloud
from states import ProfilePhotoUpdateStates

__all__ = ('register_handlers',)


async def on_start_profile_photo_update_flow(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.set_state(ProfilePhotoUpdateStates.photo)
    await callback_query.message.edit_text('🌠 Отправьте новое фото')


async def on_profile_photo_invalid_dimensions(message: Message) -> None:
    await message.reply('❌ Фото должно быть квадратным')


async def on_profile_photo_input(
        message: Message,
        state: FSMContext,
        bot: Bot,
        user: User,
        user_repository: UserRepository,
) -> None:
    photo = message.photo[-1]
    await state.clear()
    file = await bot.get_file(photo.file_id)
    file_url = bot.session.api.file_url(bot.token, file.file_path)
    new_profile_photo_url = await upload_photo_to_cloud(file_url)

    secret_message_theme_id = None
    if user.secret_message_theme is not None:
        secret_message_theme_id = user.secret_message_theme.id

    await user_repository.upsert(
        user_id=user.id,
        fullname=user.fullname,
        username=user.username,
        can_be_added_to_contacts=user.can_be_added_to_contacts,
        secret_messages_theme_id=secret_message_theme_id,
        can_receive_notifications=user.can_receive_notifications,
        profile_photo_url=new_profile_photo_url,
    )
    await message.reply('✅ Фото обновлено')


def register_handlers(router: Router) -> None:
    router.callback_query.register(
        on_start_profile_photo_update_flow,
        F.data == 'update-profile-photo',
        StateFilter('*'),
    )
    router.message.register(
        on_profile_photo_invalid_dimensions,
        F.photo,
        F.chat.type == ChatType.PRIVATE,
        invert_f(PhotoDimensionsFilter(max_ratio=1.4)),
        StateFilter(ProfilePhotoUpdateStates.photo),
    )
    router.message.register(
        on_profile_photo_input,
        F.photo,
        F.chat.type == ChatType.PRIVATE,
        PhotoDimensionsFilter(max_ratio=1.4),
        StateFilter(ProfilePhotoUpdateStates.photo),
    )
