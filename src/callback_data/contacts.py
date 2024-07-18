from aiogram.filters.callback_data import CallbackData

__all__ = ('ContactCreateCallbackData',)


class ContactCreateCallbackData(CallbackData, prefix='contact-create'):
    user_id: int
