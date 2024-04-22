from datetime import date
from uuid import UUID

from exceptions import ServerAPIError, UserDoesNotExistError
from models import User
from repositories import APIRepository

__all__ = ('UserRepository',)


class UserRepository(APIRepository):

    async def get_by_id(self, user_id: int) -> User:
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
        return User.model_validate(response_data)

    async def upsert(
            self,
            *,
            user_id: int,
            fullname: str,
            username: str | None,
            can_be_added_to_contacts: bool | None = None,
            theme_id: UUID | None = None,
            can_receive_notifications: bool | None = None,
            profile_photo_url: str | None = None,
            is_from_private_chat: bool | None = None,
            born_on: date | None = None,
    ) -> tuple[User, bool]:
        request_data = {
            'id': user_id,
            'fullname': fullname,
            'username': username,
        }
        if can_be_added_to_contacts is not None:
            request_data['can_be_added_to_contacts'] = can_be_added_to_contacts
        if theme_id is not None:
            request_data['theme_id'] = str(theme_id)
        if can_receive_notifications is not None:
            request_data['can_receive_notifications'] = (
                can_receive_notifications
            )
        if profile_photo_url is not None:
            request_data['profile_photo_url'] = profile_photo_url
        if is_from_private_chat:
            request_data['is_from_private_chat'] = is_from_private_chat
        if born_on is not None:
            request_data['born_on'] = born_on.isoformat()

        url = '/users/'
        response = await self._http_client.post(url, json=request_data)

        if response.status_code == 201:
            response_data = response.json()['result']
            return User.model_validate(response_data), True

        if response.status_code == 200:
            response_data = response.json()['result']
            return User.model_validate(response_data), False

        raise ServerAPIError
