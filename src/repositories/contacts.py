from pydantic import TypeAdapter

from models import (
    Contact,
    ContactBirthday,
    UserContact,
    UserContacts,
)
from repositories import handle_server_api_errors
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
    ) -> Contact:
        """
        Create contact between two users.

        Keyword Args:
            of_user_id: User ID of the user who creates the contact.
            to_user_id: User ID of the user to whom the contact is created.
            private_name: Private name of the contact.
            public_name: Public name of the contact.

        Returns:
            Contact model.

        Raises:
            ContactAlreadyExistsError - if contact already exists.
            ServerAPIError - if server response is not valid.
        """
        request_data = {
            'of_user_id': of_user_id,
            'to_user_id': to_user_id,
            'private_name': private_name,
            'public_name': public_name,
        }
        url = '/contacts/'
        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response.is_success:
            return Contact.model_validate(response_data)

        handle_server_api_errors(response_data['errors'])

    async def get_by_user_id(
            self,
            user_id: int,
    ) -> UserContacts:
        """
        Get user's specific contacts.

        Args:
            user_id: User Telegram ID.

        Returns:
            UserContacts model.

        Raises:
            ServerAPIError - if server response is not valid.
        """
        url = f'/contacts/users/{user_id}/'
        response = await self._http_client.get(url)

        response_data = response.json()

        if response.is_success:
            return UserContacts.model_validate(response_data)

        handle_server_api_errors(response_data['errors'])

    async def get_by_id(self, contact_id: int) -> UserContact:
        """
        Get contact by ID.

        Args:
            contact_id: Contact ID.

        Returns:
            UserContact model.

        Raises:
            ContactDoesNotExistError - if contact does not exist.
            ServerAPIError - if server response is not valid.
        """
        url = f'/contacts/{contact_id}/'
        response = await self._http_client.get(url)

        response_data = response.json()

        if response.is_success:
            return UserContact.model_validate(response_data)

        handle_server_api_errors(response_data['errors'])

    async def get_birthdays(self, user_id: int) -> list[ContactBirthday]:
        """
        Get user's contacts birthdays.

        Args:
            user_id: User Telegram ID.

        Returns:
            List of ContactBirthday models.

        Raises:
            ServerAPIError - if server response is not valid.
        """
        url = f'/users/{user_id}/contact-birthdays/'
        response = await self._http_client.get(url)

        response_data = response.json()

        if response.is_success:
            type_adapter = TypeAdapter(list[ContactBirthday])
            return type_adapter.validate_python(response_data['birthdays'])

        handle_server_api_errors(response_data['errors'])
