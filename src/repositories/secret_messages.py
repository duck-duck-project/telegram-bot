from uuid import UUID

import models
from exceptions import SecretMessageDoesNotExistError
from repositories import APIRepository

__all__ = ('SecretMessageRepository',)


class SecretMessageRepository(APIRepository):

    async def create(
            self,
            *,
            secret_message_id: UUID,
            text: str,
            sender_id: int,
            recipient_id: int,
    ) -> models.SecretMessage:
        request_data = {
            'id': str(secret_message_id),
            'text': text,
            'sender_id': sender_id,
            'recipient_id': recipient_id,
        }
        url = '/secret-messages/'

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        return models.SecretMessage.model_validate(response_data['result'])

    async def get_by_id(self, secret_message_id: UUID) -> models.SecretMessage:
        url = f'/secret-messages/{str(secret_message_id)}/'
        response = await self._http_client.get(url)

        if response.status_code == 404:
            raise SecretMessageDoesNotExistError

        response_data = response.json()

        return models.SecretMessage.model_validate(response_data['result'])

    async def update(
            self,
            *,
            secret_message_id: UUID,
            is_seen: bool | None = None,
    ) -> models.SecretMessage:
        url = f'/secret-messages/{str(secret_message_id)}/'
        request_data = {}
        if is_seen is not None:
            request_data['is_seen'] = is_seen

        response = await self._http_client.patch(url, json=request_data)

        if response.status_code == 404:
            raise SecretMessageDoesNotExistError

        response_data = response.json()

        return models.SecretMessage.model_validate(response_data['result'])

    async def delete_by_id(self, secret_message_id: UUID) -> None:
        url = f'/secret-messages/{str(secret_message_id)}/'
        response = await self._http_client.delete(url)

        if response.status_code == 404:
            raise SecretMessageDoesNotExistError
