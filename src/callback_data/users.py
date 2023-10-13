from aiogram.filters.callback_data import CallbackData

__all__ = ('UserUpdateCallbackData',)


class UserUpdateCallbackData(CallbackData, prefix='user-update'):
    field: str
