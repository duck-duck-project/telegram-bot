from uuid import UUID

from pydantic import TypeAdapter

from exceptions import ServerAPIError, ThemeDoesNotExistError
from models import Theme
from repositories.base import APIRepository

__all__ = ('ThemeRepository',)


class ThemeRepository(APIRepository):

    async def get_all(self) -> list[Theme]:
        response = await self._http_client.get('/themes/')
        if response.status_code != 200:
            raise ServerAPIError

        response_data = response.json()
        type_adapter = TypeAdapter(list[Theme])
        return type_adapter.validate_python(response_data['result'])

    async def get_by_id(self, theme_id: UUID) -> Theme:
        url = f'/themes/{str(theme_id)}/'
        response = await self._http_client.get(url)
        if response.status_code == 404:
            raise ThemeDoesNotExistError
        if response.status_code != 200:
            raise ServerAPIError
        response_data = response.json()
        return Theme.model_validate(response_data['result'])
