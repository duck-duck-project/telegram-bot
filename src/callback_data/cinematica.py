from aiogram.filters.callback_data import CallbackData

__all__ = ('MovieDetailCallbackData',)


class MovieDetailCallbackData(CallbackData, prefix='movie-detail'):
    movie_id: int
