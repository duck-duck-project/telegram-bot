import httpx
from pydantic import TypeAdapter

from models.weather import GeoCoordinates


__all__ = ('WeatherRepository',)


class WeatherRepository:

    def __init__(self, api_key: str, http_client: httpx.AsyncClient):
        self.__api_key = api_key
        self.__http_client = http_client

    async def get_coordinates(
            self,
            city_name: str,
            *,
            limit: int = 5,
    ) -> list[GeoCoordinates]:
        request_query_params = {
            'q': city_name,
            'appid': self.__api_key,
            'limit': limit,
        }
        url = 'https://api.openweathermap.org/geo/1.0/direct'
        response = await self.__http_client.get(
            url=url,
            params=request_query_params,
        )
        response_data = response.json()
        type_adapter = TypeAdapter(list[GeoCoordinates])
        return type_adapter.validate_python(response_data)

    async def get_forecast(self, coordinates: GeoCoordinates):
        request_query_params = {
            'lat': coordinates.latitude,
            'lon': coordinates.longitude,
            'appid': self.__api_key,
            'units': 'metric',
        }
        url = f'https://api.openweathermap.org/data/2.5/forecast'
        response = await self.__http_client.get(
            url=url,
            params=request_query_params,
        )
        return response.json()
