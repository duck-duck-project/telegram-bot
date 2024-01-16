from aiogram.filters.callback_data import CallbackData

__all__ = ('FoodMenuDetailCallbackData',)


class FoodMenuDetailCallbackData(CallbackData, prefix='food-menu'):
    days_skip_count: int
