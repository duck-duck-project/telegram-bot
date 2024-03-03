import random

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from callback_data import MovieDetailCallbackData
from services import get_movie_by_id, get_movies_soon, get_movies_today
from views import (
    MovieDetailView,
    MoviesSoonListView,
    MoviesTodayListView,
    answer_photo_view,
    answer_view,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower().in_({
        'случайный фильм',
        'куда сходить',
        'что посмотреть',
        'рандомный фильм',
    }),
    StateFilter('*'),
)
async def on_random_movie(message: Message) -> None:
    movies = await get_movies_today()
    view = MovieDetailView(random.choice(movies))
    await answer_photo_view(message=message, view=view)


@router.callback_query(
    MovieDetailCallbackData.filter(),
    StateFilter('*'),
)
async def on_show_movie_detail(
        callback_query: CallbackQuery,
        callback_data: MovieDetailCallbackData,
) -> None:
    loading_message = await callback_query.message.edit_text(
        text='<i>Загрузка...</i>',
    )
    movie = await get_movie_by_id(callback_data.movie_id)
    view = MovieDetailView(movie)
    try:
        await answer_photo_view(message=callback_query.message, view=view)
    finally:
        await loading_message.delete()


@router.message(
    F.text.lower().in_({
        'сегодня в кино',
        'фильмы сегодня',
        'кино сегодня',
    }),
    StateFilter('*'),
)
async def on_show_movies_today_list(
        message: Message,
) -> None:
    movies = await get_movies_today()
    view = MoviesTodayListView(movies)
    await answer_view(message=message, view=view)


@router.message(
    F.text.lower().in_({
        'скоро в кино',
        'фильмы скоро',
        'кино скоро',
    }),
    StateFilter('*'),
)
async def on_show_movies_soon_list(
        message: Message,
) -> None:
    movies = await get_movies_soon()
    view = MoviesSoonListView(movies)
    await answer_view(message=message, view=view)
