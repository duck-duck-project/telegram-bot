from models import (
    Relationship, RelationshipBreakUpResult,
    RelationshipCreateResult,
)
from repositories import APIRepository, handle_server_api_errors

__all__ = ('RelationshipRepository',)


class RelationshipRepository(APIRepository):

    async def get_by_id(self, user_id: int) -> Relationship:
        url = f'/relationships/users/{user_id}/'
        response = await self._http_client.get(url)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return Relationship.model_validate(response_data)

    async def create(
            self,
            from_user_id: int,
            to_user_id: int,
    ) -> RelationshipCreateResult:
        url = '/relationships/'
        request_data = {
            'first_user_id': from_user_id,
            'second_user_id': to_user_id,
        }
        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return RelationshipCreateResult.model_validate(response_data)

    async def break_up(self, user_id: int) -> RelationshipBreakUpResult:
        url = f'/relationships/users/{user_id}/'
        response = await self._http_client.delete(url)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return RelationshipBreakUpResult.model_validate(response_data)
