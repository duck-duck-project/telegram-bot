from models import User
from repositories import APIRepository, handle_server_api_errors

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

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return User.model_validate(response_data)

    async def create(
            self,
            *,
            user_id: int,
            fullname: str,
            username: str | None,
            is_from_private_chat: bool | None = None,
    ) -> User:
        request_data = {
            'id': user_id,
            'fullname': fullname,
            'username': username,
            'is_from_private_chat': is_from_private_chat,
        }

        url = '/users/'

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return User.model_validate(response_data)
