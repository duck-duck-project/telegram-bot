from pydantic import TypeAdapter

import models
from exceptions import (
    ContactAlreadyExistsError,
    ContactDoesNotExistError,
    InsufficientFundsForWithdrawalError,
    ServerAPIError,
    UserDoesNotExistError,
)
from models import ContactBirthday
from repositories.base import APIRepository

__all__ = ('ContactRepository',)


class ContactRepository(APIRepository):

    async def create(
            self,
            *,
            of_user_id: int,
            to_user_id: int,
            private_name: str,
            public_name: str
    ) -> models.Contact:
        request_data = {
            'of_user_id': of_user_id,
            'to_user_id': to_user_id,
            'private_name': private_name,
            'public_name': public_name,
        }
        url = '/contacts/'
        response = await self._http_client.post(url, json=request_data)
        if response.status_code == 400:
            response_data = response.json()
            error_detail = response_data.get('detail')
            if error_detail == 'Insufficient funds for contact creation':
                amount = response_data['amount']
                raise InsufficientFundsForWithdrawalError(amount=amount)
        if response.status_code == 404:
            raise UserDoesNotExistError(user_id=of_user_id)
        if response.status_code == 409:
            raise ContactAlreadyExistsError
        if response.status_code != 201:
            raise ServerAPIError
        response_data = response.json()
        return models.Contact.model_validate(response_data)

    async def get_by_user_id(
            self,
            user_id: int,
    ) -> list[models.Contact]:
        url = f'/users/{user_id}/contacts/'
        response = await self._http_client.get(url)
        if response.status_code != 200:
            raise ServerAPIError
        response_data = response.json()
        type_adapter = TypeAdapter(list[models.Contact])
        return type_adapter.validate_python(response_data)

    async def get_by_id(self, contact_id: int) -> models.Contact:
        url = f'/contacts/{contact_id}/'
        response = await self._http_client.get(url)
        if response.status_code == 404:
            raise ContactDoesNotExistError(contact_id=contact_id)
        response_data = response.json()
        return models.Contact.model_validate(response_data)

    async def get_birthdays(self, user_id: int) -> list[ContactBirthday]:
        url = f'/users/{user_id}/contact-birthdays/'
        response = await self._http_client.get(url)
        if response.is_error:
            raise ServerAPIError
        response_data = response.json()
        type_adapter = TypeAdapter(list[ContactBirthday])
        return type_adapter.validate_python(response_data['result'])
