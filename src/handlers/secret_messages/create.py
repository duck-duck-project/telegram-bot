from uuid import UUID

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import ChosenInlineResult, Message

from filters import secret_message_valid_format_chosen_inline_result_filter
from repositories import (SecretMessageRepository)
from views import (
    SecretMessageNotificationView,
    SecretMessagePromptView,
    answer_view,
    send_view,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    or_f(
        F.text.startswith('/secret_message'),
        F.text == '📩 Секретное сообщение',
    ),
    StateFilter('*'),
)
async def on_show_inline_query_prompt(message: Message) -> None:
    await answer_view(message=message, view=SecretMessagePromptView())


@router.chosen_inline_result(
    secret_message_valid_format_chosen_inline_result_filter,
    StateFilter('*'),
)
async def on_message_created(
        chosen_inline_result: ChosenInlineResult,
        state: FSMContext,
        secret_message_repository: SecretMessageRepository,
        recipient_id: int,
        bot: Bot,
):
    state_data = await state.get_data()
    secret_message_id = UUID(state_data['secret_message_id'])
    text: str = chosen_inline_result.query

    if not (0 < len(text) <= 200):
        return

    secret_message = await secret_message_repository.create(
        secret_message_id=secret_message_id,
        text=text,
        sender_id=chosen_inline_result.from_user.id,
        recipient_id=recipient_id,
    )

    if secret_message.recipient.can_receive_notifications:
        view = SecretMessageNotificationView(
            secret_message_id=secret_message.id,
            sender_full_name=secret_message.sender.username_or_fullname,
        )
        await send_view(
            bot=bot,
            chat_id=recipient_id,
            view=view,
        )
