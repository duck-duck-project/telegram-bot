from exceptions import ServerAPIError
from models import Deposit
from repositories import APIRepository

__all__ = ('DepositRepository',)


class DepositRepository(APIRepository):

    async def create(
            self,
            *,
            user_id: int,
            amount: int,
            description: str,
    ) -> Deposit:
        url = '/economics/deposit/'
        request_data = {
            'user_id': user_id,
            'amount': amount,
            'description': description,
        }
        async with self._http_client.post(url, json=request_data) as response:
            if response.status != 201:
                raise ServerAPIError
            response_data = await response.json()
        return Deposit.model_validate(response_data)
