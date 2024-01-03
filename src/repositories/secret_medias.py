from uuid import UUID

import models
from exceptions import (
    SecretMediaAlreadyExistsError,
    SecretMediaDoesNotExistError,
)
from repositories import APIRepository

__all__ = ('SecretMediaRepository',)


class SecretMediaRepository(APIRepository):

    async def create(
            self,
            media_type: int,
            file_id: str,
            description: str | None,
            contact_id: int,
    ) -> models.SecretMedia:
        url = '/secret-medias/'
        request_data = {
            'media_type': media_type,
            'file_id': file_id,
            'name': description,
            'contact_id': contact_id,
        }
        response = await self._http_client.post(url, json=request_data)
        if response.status_code == 409:
            raise SecretMediaAlreadyExistsError
        response_data = response.json()
        return models.SecretMedia.model_validate(response_data)

    async def get_by_id(self, secret_media_id: UUID) -> models.SecretMedia:
        url = f'/secret-medias/{secret_media_id}/'
        response = await self._http_client.get(url)
        if response.status_code == 404:
            raise SecretMediaDoesNotExistError
        response_data = response.json()
        return models.SecretMedia.model_validate(response_data)
