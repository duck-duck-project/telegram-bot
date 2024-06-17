from exceptions import NotEnoughEnergyError, ServerAPIError
from exceptions.mining import MiningActionThrottlingError
from models import MinedResourceResult, MiningUserStatistics
from repositories import APIRepository

__all__ = ('MiningRepository',)


class MiningRepository(APIRepository):

    async def mine(self, user_id: int) -> MinedResourceResult:
        url = '/mining/'
        request_data = {'user_id': user_id}
        response = await self._http_client.post(url, json=request_data)
        response_data = response.json()
        if response_data.get('ok'):
            return MinedResourceResult.model_validate(response_data['result'])
        if 'next_mining_in_seconds' in response_data:
            next_mining_in_seconds = response_data['next_mining_in_seconds']
            raise MiningActionThrottlingError(int(next_mining_in_seconds))
        if 'required_energy' in response_data:
            required_energy = int(response_data['required_energy'])
            raise NotEnoughEnergyError(required_energy)
        raise ServerAPIError

    async def get_user_statistics(self, user_id: int) -> MiningUserStatistics:
        url = '/mining/user-statistics/'
        query_params = {'user_id': user_id}
        response = await self._http_client.get(url, params=query_params)
        response_data = response.json()
        if response_data.get('ok'):
            return MiningUserStatistics.model_validate(response_data['result'])
        raise ServerAPIError
