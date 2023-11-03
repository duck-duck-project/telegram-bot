from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User

from repositories import BalanceRepository
from services import AnonymousMessageSender
from states import AnonymousMessagingStates
from views import (
    AnonymousMessagingToggledInGroupChatView,
    AnonymousMessagingEnabledView,
)
from views import answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    or_f(
        F.photo,
        F.audio,
        F.voice,
        F.animation,
        F.document,
        F.video,
        F.video_note,
        F.sticker,
    ),
    F.chat.type == ChatType.PRIVATE,
    StateFilter(AnonymousMessagingStates.enabled),
)
async def on_media_for_retranslation(
        message: Message,
        chat_id_for_retranslation: int | str,
        anonymous_message_sender: AnonymousMessageSender,
        balance_repository: BalanceRepository,
) -> None:
    await balance_repository.create_withdrawal(
        user_id=message.from_user.id,
        amount=10000,
        description='Анонимное медиа',
    )
    await anonymous_message_sender.send_media(
        chat_id=chat_id_for_retranslation,
        message=message,
    )


@router.message(
    F.text,
    F.chat.type == ChatType.PRIVATE,
    StateFilter(AnonymousMessagingStates.enabled),
)
async def on_send_anonymous_text(
        message: Message,
        chat_id_for_retranslation: int | str,
        anonymous_message_sender: AnonymousMessageSender,
        balance_repository: BalanceRepository,
) -> None:
    await balance_repository.create_withdrawal(
        user_id=message.from_user.id,
        amount=5000,
        description='Анонимное сообщение',
    )
    await anonymous_message_sender.send_text(
        chat_id=chat_id_for_retranslation,
        message=message,
    )


@router.message(
    Command('anonymous_messaging'),
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    StateFilter('*'),
)
async def on_toggle_anonymous_messaging_mode_in_group_chat(
        message: Message,
        bot_user: User,
) -> None:
    view = AnonymousMessagingToggledInGroupChatView(bot_user.username)
    await answer_view(message=message, view=view)


@router.message(
    F.text.in_({
        '/anonymous_messaging',
        '🔐 Включить анонимные сообщения',
    }),
    F.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
async def on_toggle_anonymous_messaging_mode(
        message: Message,
        state: FSMContext,
) -> None:
    await state.set_state(AnonymousMessagingStates.enabled)
    view = AnonymousMessagingEnabledView()
    await answer_view(message=message, view=view)
