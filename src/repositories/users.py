from datetime import date
from uuid import UUID

from enums import Gender, PersonalityTypePrefix, PersonalityTypeSuffix
from exceptions import (
    NotEnoughEnergyError,
    NotEnoughHealthError,
    ServerAPIError,
    SportActivitiesThrottledError,
    UserDoesNotExistError,
)
from models import User, UserEnergyRefill, UserSportsActivityResult
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
            personality_type_prefix: PersonalityTypePrefix | None = None,
            personality_type_suffix: PersonalityTypeSuffix | None = None,
            real_first_name: str | None = None,
            real_last_name: str | None = None,
            patronymic: str | None = None,
            gender: Gender | None = None,
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
        if personality_type_prefix is not None:
            request_data['personality_type_prefix'] = personality_type_prefix
        if personality_type_suffix is not None:
            request_data['personality_type_suffix'] = personality_type_suffix
        if real_first_name is not None:
            request_data['real_first_name'] = real_first_name
        if real_last_name is not None:
            request_data['real_last_name'] = real_last_name
        if patronymic is not None:
            request_data['patronymic'] = patronymic
        if gender is not None:
            request_data['gender'] = gender

        url = '/users/'
        response = await self._http_client.post(url, json=request_data)

        if response.status_code == 201:
            response_data = response.json()['result']
            return User.model_validate(response_data), True

        if response.status_code == 200:
            response_data = response.json()['result']
            return User.model_validate(response_data), False

        raise ServerAPIError

    async def consume_food(
            self,
            *,
            user_id: int,
            energy: int,
            health_impact_value: int
    ) -> UserEnergyRefill:
        url = '/users/consume-food/'
        request_data = {
            'user_id': user_id,
            'energy': energy,
            'health_impact_value': health_impact_value,
        }
        response = await self._http_client.post(url, json=request_data)
        response_data = response.json()

        if 'required_health' in response_data:
            required_health = int(response_data['required_health'])
            raise NotEnoughHealthError(required_health)

        if response.status_code == 200:
            return UserEnergyRefill.model_validate(response_data['result'])
        raise ServerAPIError

    async def do_sports(
            self,
            *,
            user_id: int,
            health_benefit_value: int,
            energy_cost_value: int,
    ):
        url = '/users/sports/'
        request_data = {
            'user_id': user_id,
            'health_benefit_value': health_benefit_value,
            'energy_cost_value': energy_cost_value,
        }
        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response.status_code == 200:
            result = response_data['result']
            return UserSportsActivityResult.model_validate(result)

        if 'required_energy' in response_data:
            required_energy = int(response_data['required_energy'])
            raise NotEnoughEnergyError(required_energy)
        if 'next_sports_in_seconds' in response_data:
            next_sports_in_seconds = response_data['next_sports_in_seconds']
            raise SportActivitiesThrottledError(int(next_sports_in_seconds))

        raise ServerAPIError
