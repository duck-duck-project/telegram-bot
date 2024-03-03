from collections.abc import Iterable

from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, InputFile,
    URLInputFile,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_data import MovieDetailCallbackData
from models import Movie
from views import PhotoView, ReplyMarkup
from views.base import View

__all__ = ('MoviesTodayListView', 'MoviesSoonListView', 'MovieDetailView')


class MoviesListView(View):

    def __init__(self, movies: Iterable[Movie]):
        self.__movies = tuple(movies)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        for movie in self.__movies:
            callback_data = MovieDetailCallbackData(movie_id=movie.id).pack()

            text = movie.name
            if movie.age_restriction:
                text = f'{text} ({movie.age_restriction})'

            if movie.is_hit:
                text = f'🔥 {text}'

            button = InlineKeyboardButton(
                text=text,
                callback_data=callback_data,
            )
            keyboard.row(button)

        return keyboard.as_markup()


class MoviesTodayListView(MoviesListView):
    text = '<b>🔥 Сегодня в кино</b>'


class MoviesSoonListView(MoviesListView):
    text = '<b>🚀 Скоро в кино</b>'


class MovieDetailView(PhotoView):

    def __init__(self, movie: Movie):
        self.__movie = movie

    def get_photo(self) -> str | InputFile:
        url = f'https://cinematica.kg{self.__movie.file_poster_vertical}'
        return URLInputFile(url)

    def get_caption(self) -> str:
        lines: list[str] = []

        if self.__movie.is_hit:
            lines.append('<b>🔥Хит 🔥</b>')

        lines.append(f'<b>Название:</b> {self.__movie.name}')

        for detail in self.__movie.details:
            lines.append(f'<b>{detail.title}</b>: {detail.value}')

        if self.__movie.age_restriction:
            lines.append(f'<b>Ограничение:</b> {self.__movie.age_restriction}')

        lines.append(
            f'<b>Прокат:</b>'
            f' {self.__movie.premiere_starts_at:%d.%m.%Y}'
            f'-{self.__movie.premiere_ends_at:%d.%m.%Y}'
        )

        has_rating = self.__movie.rating is not None
        has_votes = self.__movie.vote_count is not None
        if has_rating and has_votes:
            lines.append(
                f'<b>Рейтинг:</b> {self.__movie.rating:.1f}'
                f' ({self.__movie.vote_count} голосов)'
            )

        if self.__movie.long_description:
            lines.append(f'<b>Описание:</b> {self.__movie.long_description}')

        return '\n'.join(lines)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()

        if self.__movie.file_trailer is not None:
            trailer_url = f'https://cinematica.kg{self.__movie.file_trailer}'
            keyboard.row(
                InlineKeyboardButton(
                    text='🎬 Смотреть трейлер',
                    url=trailer_url,
                ),
            )

        cinematica_url = f'https://cinematica.kg/movies/{self.__movie.id}'
        keyboard.row(
            InlineKeyboardButton(
                text='🍿 Подробнее',
                url=cinematica_url,
            ),
        )

        return keyboard.as_markup()
