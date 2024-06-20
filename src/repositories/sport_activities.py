from pydantic import TypeAdapter

from exceptions import ServerAPIError
from models import SportActivity
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

    async def do_sports(self, user_id: int, sport_activity_name: str):
        url = '/sport-activity-actions/'
        request_data = {
            'user_id': user_id,
            'sport_activity_name': sport_activity_name,
        }

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response_data.get('ok'):
            return

        raise ServerAPIError
