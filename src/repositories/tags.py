import json

from pydantic import TypeAdapter

from exceptions import (
    ServerAPIError,
    TagDoesNotBelongToUserError,
    TagDoesNotExistError,
)
from models import Tag
from repositories import APIRepository

__all__ = ('TagRepository',)


class TagRepository(APIRepository):

    async def get_all_by_user_id(self, user_id: int) -> list[Tag]:
        url = f'/users/{user_id}/tags/'
        response = await self._http_client.get(url)
        type_adapter = TypeAdapter(list[Tag])
        response_data = response.json()
        return type_adapter.validate_python(response_data['result'])

    async def create(
            self,
            *,
            of_user_id: int,
            to_user_id: int,
            text: str,
            weight,
    ) -> Tag:
        url = f'/users/tags/'
        request_data = {
            'of_user_id': of_user_id,
            'to_user_id': to_user_id,
            'text': text,
            'weight': weight,
        }
        response = await self._http_client.post(url, json=request_data)
        response_data = response.json()
        return Tag.model_validate(response_data['result'])

    async def delete(self, *, user_id: int, tag_id: int) -> bool:
        url = f'/users/{user_id}/tags/{tag_id}/'
        response = await self._http_client.delete(url)
        if response.status_code == 404:
            raise TagDoesNotExistError
        if response.status_code == 403:
            raise TagDoesNotBelongToUserError
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            raise ServerAPIError
        return response_data.get('ok', False)
