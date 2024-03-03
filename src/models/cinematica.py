from datetime import datetime

from pydantic import BaseModel, Field

__all__ = ('Movie', 'MovieDetail')


class MovieDetail(BaseModel):
    order: int
    title: str
    value: str | int


class Movie(BaseModel):
    id: int
    name: str
    age_restriction: str
    premiere_starts_at: datetime = Field(alias='date_start')
    premiere_ends_at: datetime = Field(alias='date_end')
    details: list[MovieDetail]
    file_poster: str
    file_poster_vertical: str
    file_trailer: str | None = None
    is_hit: bool = Field(alias='hit')
    rating: float | None = None
    vote_count: int | None = None
    long_description: str | None = Field(default=None, alias='long_desc')
