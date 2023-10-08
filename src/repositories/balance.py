from exceptions import (
    ServerAPIError,
    UserDoesNotExistError,
    InsufficientFundsForWithdrawalError,
    InsufficientFundsForTransferError,
)
from models import SystemTransaction, UserBalance, Transfer
from repositories.base import APIRepository

__all__ = ('BalanceRepository',)


class BalanceRepository(APIRepository):

    async def create_transfer(
            self,
            *,
            sender_id: int,
            recipient_id: int,
            amount: float,
            description: str | None = None,
    ) -> Transfer:
        url = '/economics/transfers/'
        request_data = {
            'sender_id': sender_id,
            'recipient_id': recipient_id,
            'amount': amount,
            'description': description,
        }
        async with self._http_client.post(url, json=request_data) as response:
            if response.status == 400:
                response_data = await response.json()
                if response_data[0] == 'Insufficient funds for transfer':
                    raise InsufficientFundsForTransferError
            if response.status != 201:
                raise ServerAPIError
            response_data = await response.json()
        return Transfer.model_validate(response_data)

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

    async def create_richest_users_statistics_task(
            self,
            chat_id: int,
            user_id: int,
    ) -> None:
        url = '/economics/richest-users-statistics/'
        request_data = {
            'limit': 50,
            'chat_id': chat_id,
            'user_id': user_id,
        }
        async with self._http_client.post(url, json=request_data) as response:
            if response.status != 202:
                raise ServerAPIError
