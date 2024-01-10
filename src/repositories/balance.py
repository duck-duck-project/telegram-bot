from uuid import UUID

from exceptions import (
    ServerAPIError,
    UserDoesNotExistError,
    InsufficientFundsForWithdrawalError,
    InsufficientFundsForTransferError,
    TransactionDoesNotExistError,
    TransferRollbackExpiredError,
    TransactionDoesNotBelongToUserError,
    InsufficientFundsForTransferRollbackError,
)
from models import SystemTransaction, UserBalance, Transfer
from repositories.base import APIRepository

__all__ = ('BalanceRepository',)


class BalanceRepository(APIRepository):

    async def rollback_transfer(
            self,
            *,
            transfer_id: UUID,
            user_id: int,
    ) -> None:
        request_query_params = {
            'transaction_id': str(transfer_id),
            'user_id': user_id,
        }
        url = '/economics/transfers/'
        response = await self._http_client.delete(
            url=url,
            params=request_query_params,
        )
        if response.status_code == 404:
            raise TransactionDoesNotExistError
        if response.status_code == 400:
            match response.json():
                case ['Transfer rollback time expired']:
                    raise TransferRollbackExpiredError
                case ['Transaction does not belong to user']:
                    raise TransactionDoesNotBelongToUserError
                case ['Insufficient funds for transfer rollback']:
                    raise InsufficientFundsForTransferRollbackError

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
        response = await self._http_client.post(url, json=request_data)
        if response.status_code == 400:
            response_data = response.json()
            if response_data[0] == 'Insufficient funds for transfer':
                raise InsufficientFundsForTransferError
        if response.status_code != 201:
            raise ServerAPIError
        response_data = response.json()
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
        response = await self._http_client.post(url, json=request_data)
        if response.status_code == 400:
            response_data = response.json()
            if response_data[0] == 'Insufficient funds for withdrawal':
                raise InsufficientFundsForWithdrawalError(amount=amount)
        if response.status_code != 201:
            raise ServerAPIError
        response_data = response.json()
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
        response = await self._http_client.post(url, json=request_data)
        if response.status_code != 201:
            raise ServerAPIError
        response_data = response.json()
        return SystemTransaction.model_validate(response_data)

    async def get_user_balance(self, user_id: int) -> UserBalance:
        url = f'/economics/balance/users/{user_id}/'
        response = await self._http_client.get(url)
        if response.status_code == 404:
            raise UserDoesNotExistError(user_id=user_id)
        if response.status_code != 200:
            raise ServerAPIError
        response_data = response.json()
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
        response = await self._http_client.post(url, json=request_data)
        if response.status_code != 202:
            raise ServerAPIError
