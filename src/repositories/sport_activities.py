from pydantic import TypeAdapter

from exceptions import (
    NotEnoughEnergyError, NotEnoughHealthError,
    ServerAPIError, SportActivityDoesNotExistError,
    SportActivityOnCooldownError,
)
from models import SportActivity, SportActivityActionResult
from repositories import APIRepository

__all__ = ('SportActivityRepository',)


class SportActivityRepository(APIRepository):

    async def get_all(self) -> tuple[SportActivity, ...]:
        url = '/sport-activities/'

        response = await self._http_client.get(url)

        response_data = response.json()

        if response_data.get('ok'):
            type_adapter = TypeAdapter(tuple[SportActivity, ...])
            return type_adapter.validate_python(response_data['result'])

        raise ServerAPIError

    async def do_sports(
            self,
            user_id: int,
            sport_activity_name: str,
    ) -> SportActivityActionResult:
        url = '/sport-activity-actions/'
        request_data = {
            'user_id': user_id,
            'sport_activity_name': sport_activity_name,
        }

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response_data.get('detail') == 'Sport activity does not exist':
            raise SportActivityDoesNotExistError(
                sport_activity_name=response_data['sport_activity_name'],
            )

        if response_data.get('detail') == 'Sport activity is on cooldown':
            raise SportActivityOnCooldownError(
                next_activity_in_seconds=int(
                    response_data['next_activity_in_seconds']
                ),
            )

        if response_data.get('detail') == 'Not enough energy':
            raise NotEnoughEnergyError(
                required_energy=int(response_data['required_energy_value']),
            )

        if response_data.get('ok'):
            return SportActivityActionResult.model_validate(
                response_data['result'],
            )

        raise ServerAPIError
