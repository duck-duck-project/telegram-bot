from exceptions import (
    ServerAPIError, UserDoesNotExistError,
    InsufficientFundsForWithdrawalError
)
from models import SystemTransaction, UserBalance
from repositories.base import APIRepository

__all__ = ('BalanceRepository',)


class BalanceRepository(APIRepository):

    async def create_withdrawal(
            self,
            *,
            user_id: int,
            amount: int,
            description: str,
    ) -> SystemTransaction:
        url = '/economics/withdraw/'
        request_data = {
            'user_id': user_id,
            'amount': amount,
            'description': description,
        }
        async with self._http_client.post(url, json=request_data) as response:
            if response.status == 400:
                response_data = await response.json()
                if response_data[0] == 'Insufficient funds for withdrawal':
                    raise InsufficientFundsForWithdrawalError
            if response.status != 201:
                raise ServerAPIError
            response_data = await response.json()
        return SystemTransaction.model_validate(response_data)

    async def create_deposit(
            self,
            *,
            user_id: int,
            amount: int,
            description: str,
    ) -> SystemTransaction:
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
        return SystemTransaction.model_validate(response_data)

    async def get_user_balance(self, user_id: int) -> UserBalance:
        url = f'/economics/balance/users/{user_id}/'
        async with self._http_client.get(url) as response:
            if response.status == 404:
                raise UserDoesNotExistError(user_id=user_id)
            if response.status != 200:
                raise ServerAPIError
            response_data = await response.json()
        return UserBalance.model_validate(response_data)
