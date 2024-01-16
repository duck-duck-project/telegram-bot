from uuid import UUID

from aiogram.filters.callback_data import CallbackData

__all__ = ('TransferRollbackCallbackData',)


class TransferRollbackCallbackData(CallbackData, prefix='transfer_rollback'):
    transfer_id: UUID
