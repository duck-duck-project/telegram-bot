from exceptions import ServerAPIError
from exceptions.mining import MiningActionThrottlingError
from models import MinedResource
from repositories import APIRepository

__all__ = ('MiningRepository',)


class MiningRepository(APIRepository):

    async def mine(self, user_id: int) -> MinedResource:
        url = '/mining/'
        request_data = {'user_id': user_id}
        response = await self._http_client.post(url, json=request_data)
        response_data = response.json()
        if response_data.get('ok'):
            return MinedResource.model_validate(response_data['result'])
        if next_mining_in_seconds := int(
                response_data.get('next_mining_in_seconds')
        ):
            raise MiningActionThrottlingError(next_mining_in_seconds)
        raise ServerAPIError