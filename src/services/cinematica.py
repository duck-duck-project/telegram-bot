import httpx
from pydantic import TypeAdapter

from models import Movie

__all__ = (
    'get_movies_today',
    'get_movies_soon',
    'get_movie_by_id',
)


async def get_movies(url: str) -> list[Movie]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    response.raise_for_status()
    response_data = response.json()

    movies = response_data['list']

    type_adapter = TypeAdapter(list[Movie])
    return type_adapter.validate_python(movies)


async def get_movies_today() -> list[Movie]:
    return await get_movies('https://cinematica.kg/api/v1/movies/today')


async def get_movies_soon() -> list[Movie]:
    return await get_movies('https://cinematica.kg/api/v1/movies/soon')


async def get_movie_by_id(movie_id: int) -> Movie:
    url = f'https://cinematica.kg/api/v1/movies/{movie_id}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    response.raise_for_status()
    response_data = response.json()

    type_adapter = TypeAdapter(Movie)
    return type_adapter.validate_python(response_data)
