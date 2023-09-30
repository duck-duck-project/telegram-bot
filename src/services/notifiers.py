from aiogram import Bot

from models import SystemTransaction, Transfer
from services.services import send_view
from views import DepositNotificationView, WithdrawalNotificationView

__all__ = ('Notifier', 'BalanceNotifier',)


class Notifier:

    def __init__(self, bot: Bot):
        self._bot = bot


class BalanceNotifier(Notifier):

    async def send_deposit_notification(
            self,
            deposit: SystemTransaction,
    ) -> None:
        view = DepositNotificationView(deposit)
        await send_view(
            bot=self._bot,
            chat_id=deposit.user.id,
            view=view,
        )

    async def send_withdrawal_notification(
            self,
            withdrawal: SystemTransaction,
    ) -> None:
        view = WithdrawalNotificationView(withdrawal)
        await send_view(
            bot=self._bot,
            chat_id=withdrawal.user.id,
            view=view,
        )

    async def send_transfer_notification(
            self,
            transfer: Transfer,
    ) -> None:
        view = WithdrawalNotificationView(transfer)
        await send_view(
            bot=self._bot,
            chat_id=transfer.sender.id,
            view=view,
        )
        view = DepositNotificationView(transfer)
        await send_view(
            bot=self._bot,
            chat_id=transfer.recipient.id,
            view=view,
        )
