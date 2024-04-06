from aiogram.filters.callback_data import CallbackData

__all__ = ('UserBalanceDetailCallbackData',)


class UserBalanceDetailCallbackData(CallbackData, prefix='user-balance-detail'):
    user_id: int
