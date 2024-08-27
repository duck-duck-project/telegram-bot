from models import MinedResourceResult, MiningUserStatistics
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

        if response.is_success:
            return MinedResourceResult.model_validate(response_data)

        handle_server_api_errors(response_data['errors'])

    async def get_user_statistics(self, user_id: int) -> MiningUserStatistics:
        url = '/mining/user-statistics/'
        query_params = {'user_id': user_id}

        response = await self._http_client.get(url, params=query_params)

        response_data = response.json()

        if response.is_success:
            return MiningUserStatistics.model_validate(response_data)

        handle_server_api_errors(response_data['errors'])
