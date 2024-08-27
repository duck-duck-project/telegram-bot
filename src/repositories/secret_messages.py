from typing import Never
from uuid import UUID

from models import SecretTextMessage
from repositories import APIRepository, handle_server_api_errors

__all__ = ('SecretMessageRepository',)


class SecretMessageRepository(APIRepository):

    async def create(
            self,
            *,
            secret_message_id: UUID,
            text: str,
            contact_id: int,
    ) -> SecretTextMessage:
        """
        Create secret text message.

        Keyword Args:
            secret_message_id: Secret message ID in UUID format.
            text: Secret message text.
            contact_id: Contact ID.

        Returns:
            SecretTextMessage object.

        Raises:
            ContactDoesNotExistError: If contact with provided
                                      ID does not exist.
            ServerAPIError: If server returned an error.
        """
        request_data = {
            'id': str(secret_message_id),
            'text': text,
            'contact_id': contact_id,
        }
        url = '/secret-messages/text/'

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response.is_success:
            return SecretTextMessage.model_validate(response_data)

        handle_server_api_errors(response_data['errors'])

    async def get_by_id(self, secret_message_id: UUID) -> SecretTextMessage:
        """
        Get secret text message by ID.

        Args:
            secret_message_id:

        Returns:
            SecretTextMessage object.

        Raises:
            SecretMessageDoesNotExistError: If secret message with provided ID
                                             does not exist.
            ServerAPIError: If server returned an error.
        """
        url = f'/secret-messages/text/{str(secret_message_id)}/'
        response = await self._http_client.get(url)

        response_data: dict = response.json()

        if response.is_success:
            return SecretTextMessage.model_validate(response_data)

        handle_server_api_errors(response_data['errors'])

    async def mark_as_seen(
            self,
            secret_message_id: UUID,
    ) -> None | Never:
        """
        Mark secret message as seen.

        Args:
            secret_message_id: Secret message ID.

        Raises:
            SecretMessageDoesNotExistError: If secret message with provided ID
                                             does not exist.
            ServerAPIError: If server returned an error.
        """
        url = f'/secret-messages/text/{str(secret_message_id)}/seen/'

        response = await self._http_client.post(url)

        if response.is_success:
            return

        response_data = response.json()
        handle_server_api_errors(response_data['errors'])

    async def delete_by_id(self, secret_message_id: UUID) -> None:
        """
        Delete secret message by ID.

        Args:
            secret_message_id: Secret message ID.

        Raises:
            SecretMessageDoesNotExistError: If secret message with provided ID
                                             does not exist.
            ServerAPIError: If server returned an error.
        """
        url = f'/secret-messages/text/{str(secret_message_id)}/'
        response = await self._http_client.delete(url)

        if response.is_success:
            return

        response_data = response.json()
        handle_server_api_errors(response_data['errors'])
