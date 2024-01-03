from datetime import date

import models
from exceptions import (
    UserDoesNotExistError,
    ServerAPIError,
    UserAlreadyExistsError,
)
from repositories import APIRepository

__all__ = ('UserRepository',)


class UserRepository(APIRepository):

    async def get_by_id(self, user_id: int) -> models.User:
        """Get user by ID.

        Args:
            user_id: User's Telegram ID.

        Returns:
            User model.

        Raises:
            UserDoesNotExistError: If user with given ID does not exist.
            ServerAPIError: If server returns unexpected response status code.
        """
        url = f'/users/{user_id}/'
        response = await self._http_client.get(url)
        if response.status_code == 404:
            raise UserDoesNotExistError(user_id=user_id)
        if response.status_code != 200:
            raise ServerAPIError
        response_data = response.json()
        return models.User.model_validate(response_data)

    async def create(
            self,
            *,
            user_id: int,
            fullname: str,
            username: str | None,
    ) -> models.User:
        """Create user on the server.

        Keyword Args:
            user_id: User's Telegram ID.
            fullname: User's full name.
            username: User's username.

        Returns:
            User model.

        Raises:
            UserAlreadyExistsError: If user with given ID already exists.
            ServerAPIError: If server returns unexpected response status code.
        """
        request_data = {
            'id': user_id,
            'fullname': fullname,
            'username': username,
        }
        url = '/users/'
        response = await self._http_client.post(url, json=request_data)
        if response.status_code == 409:
            raise UserAlreadyExistsError(user_id=user_id)
        if response.status_code != 201:
            raise ServerAPIError
        response_data = response.json()
        return models.User.model_validate(response_data)

    async def update(
            self,
            *,
            user_id: int,
            fullname: str,
            username: str | None,
            can_be_added_to_contacts: bool,
            secret_messages_theme_id: int | None,
            can_receive_notifications: bool,
            born_at: date | None,
            profile_photo_url: str | None,
    ) -> None:
        """Update user's data on the server.

        Keyword Args:
            user_id: User's Telegram ID.
            fullname: User's full name.
            username: User's username.
            can_be_added_to_contacts: Whether user can be added to contacts.
            secret_messages_theme_id: User's secret messages theme ID.
            can_receive_notifications: Whether user can receive notifications.
            born_at: User's date of birth.
            profile_photo_url: User's profile photo URL.

        Raises:
            UserDoesNotExistError: If user with given ID does not exist.
            ServerAPIError: If server returned unexpected response status code.
        """
        request_data = {
            'fullname': fullname,
            'username': username,
            'can_be_added_to_contacts': can_be_added_to_contacts,
            'secret_message_theme_id': secret_messages_theme_id,
            'can_receive_notifications': can_receive_notifications,
            'born_at': born_at.isoformat() if born_at else None,
            'profile_photo_url': profile_photo_url,
        }
        url = f'/users/{user_id}/'
        response = await self._http_client.put(url, json=request_data)
        if response.status_code == 404:
            raise UserDoesNotExistError(user_id=user_id)
        if response.status_code != 204:
            raise ServerAPIError

    async def get_or_create(
            self,
            *,
            user_id: int,
            fullname: str,
            username: str | None,
    ) -> tuple[models.User, bool]:
        try:
            return await self.get_by_id(user_id=user_id), False
        except UserDoesNotExistError:
            return await self.create(
                user_id=user_id,
                fullname=fullname,
                username=username,
            ), True
