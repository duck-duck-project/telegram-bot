from models import Tag, UserTags
from repositories import APIRepository, handle_server_api_errors

__all__ = ('TagRepository',)


class TagRepository(APIRepository):

    async def get_all_by_user_id(self, user_id: int) -> UserTags:
        url = f'/tags/users/{user_id}/'

        response = await self._http_client.get(url)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return UserTags.model_validate(response_data)

    async def create(
            self,
            *,
            of_user_id: int,
            to_user_id: int,
            text: str,
            weight,
    ) -> Tag:
        url = f'/tags/'
        request_data = {
            'of_user_id': of_user_id,
            'to_user_id': to_user_id,
            'text': text,
            'weight': weight,
        }

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return Tag.model_validate(response_data)

    async def delete(self, *, user_id: int, tag_id: int) -> None:
        url = f'/tags/'
        request_data = {
            'user_id': user_id,
            'tag_id': tag_id,
        }

        response = await self._http_client.request(
            method='DELETE',
            url=url,
            json=request_data,
        )

        if response.is_error:
            response_data = response.json()
            handle_server_api_errors(response_data['errors'])
