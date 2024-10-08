from models import (
    MinedResourceResult, MiningChatStatistics,
    MiningUserStatistics,
)
from repositories import APIRepository, handle_server_api_errors

__all__ = ('MiningRepository',)


class MiningRepository(APIRepository):

    async def mine(
            self,
            user_id: int,
            chat_id: int | None = None,
    ) -> MinedResourceResult:
        url = '/mining/'
        request_data = {'user_id': user_id}

        if chat_id is not None:
            request_data['chat_id'] = chat_id

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return MinedResourceResult.model_validate(response_data)

    async def get_user_statistics(self, user_id: int) -> MiningUserStatistics:
        url = f'/mining/users/{user_id}/statistics/'
        response = await self._http_client.get(url)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return MiningUserStatistics.model_validate(response_data)

    async def get_chat_statistics(self, chat_id: int) -> MiningChatStatistics:
        url = f'/mining/chats/{chat_id}/statistics/'
        response = await self._http_client.get(url)

        response_data = response.json()

        if response.is_success:
            handle_server_api_errors(response_data['errors'])

        return MiningChatStatistics.model_validate(response_data)
