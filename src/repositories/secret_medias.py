from uuid import UUID

import models
from exceptions import (
    SecretMediaAlreadyExistsError,
    SecretMediaDoesNotExistError,
)
from models import SecretMediaMessage
from repositories import APIRepository, handle_server_api_errors

__all__ = ('SecretMediaRepository',)


class SecretMediaRepository(APIRepository):

    async def create(
            self,
            media_type: int,
            file_id: str,
            description: str | None,
            contact_id: int,
    ) -> SecretMediaMessage:
        url = '/secret-messages/media/'
        request_data = {
            'media_type': media_type,
            'file_id': file_id,
            'caption': description,
            'contact_id': contact_id,
        }
        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response.is_success:
            return SecretMediaMessage.model_validate(response_data)

        handle_server_api_errors(response_data['errors'])

    async def get_by_id(
            self,
            secret_media_id: UUID,
    ) -> models.SecretMediaMessage:
        url = f'/secret-messages/media/{secret_media_id}/'
        response = await self._http_client.get(url)

        response_data = response.json()

        if response.is_success:
            return SecretMediaMessage.model_validate(response_data)

        handle_server_api_errors(response_data['errors'])
