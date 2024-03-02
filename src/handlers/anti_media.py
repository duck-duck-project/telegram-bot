from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, or_f, invert_f
from aiogram.types import Message

from exceptions import InsufficientFundsForWithdrawalError
from exceptions.manas_id import ManasIdDoesNotExistError
from repositories import BalanceRepository, ManasIdRepository
from services import BalanceNotifier, try_to_delete_message
from views import InsufficientFundsForSendingMediaView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    F.text,
    F.from_user.id.in_({5895029052}),
    StateFilter('*'),
)
async def on_message(
        message: Message,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    try:
        withdrawal = await balance_repository.create_withdrawal(
            user_id=message.from_user.id,
            amount=500,
            description='Отправка сообщения в групповом чате',
        )
    except InsufficientFundsForWithdrawalError:
        await try_to_delete_message(message)
    else:
        await balance_notifier.send_withdrawal_notification(withdrawal)


@router.message(
    invert_f(F.from_user.id.in_({5185621939})),
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    or_f(
        F.sticker,
        F.animation,
        F.video,
        F.voice,
        F.video_note,
    ),
    StateFilter('*'),
)
async def on_media_in_group_chat(
        message: Message,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
        manas_id_repository: ManasIdRepository,
) -> None:
    user_id = message.from_user.id

    try:
        await manas_id_repository.get_manas_id_by_user_id(user_id)
    except ManasIdDoesNotExistError:
        price = 10000
    else:
        price = 500

    try:
        withdrawal = await balance_repository.create_withdrawal(
            user_id=message.from_user.id,
            amount=price,
            description='Отправка медиа в групповом чате',
        )
    except InsufficientFundsForWithdrawalError:
        view = InsufficientFundsForSendingMediaView(user=message.from_user)
        await answer_view(view=view, message=message)
        await try_to_delete_message(message)
    else:
        await balance_notifier.send_withdrawal_notification(withdrawal)
