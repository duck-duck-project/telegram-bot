import json

from pydantic import TypeAdapter

from models import Tag
from repositories import APIRepository

__all__ = ('TagRepository',)


class TagRepository(APIRepository):

    async def get_all_by_user_id(self, user_id: int) -> list[Tag]:
        url = f'/users/{user_id}/tags/'
        response = await self._http_client.get(url)
        type_adapter = TypeAdapter(list[Tag])
        response_data = response.json()
        return type_adapter.validate_python(response_data)

    async def create(
            self,
            *,
            of_user_id: int,
            to_user_id: int,
            text: str,
            weight,
    ) -> Tag:
        url = f'/users/{of_user_id}/tags/'
        request_data = {
            'to_user_id': to_user_id,
            'text': text,
            'weight': weight,
        }
        response = await self._http_client.post(url, json=request_data)
        response_data = response.json()
        return Tag.model_validate(response_data)

    async def delete(self, tag_id: int) -> bool:
        url = f'/users/tags/{tag_id}/'
        response = await self._http_client.delete(url)
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            return False
        return response_data.get('ok', False)
