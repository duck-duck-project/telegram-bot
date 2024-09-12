from pydantic import TypeAdapter

from models import SportActivity, SportActivityActionResult
from repositories import APIRepository, handle_server_api_errors

__all__ = ('SportActivityRepository',)


class SportActivityRepository(APIRepository):

    async def get_all(self) -> tuple[SportActivity, ...]:
        url = '/sport-activities/'

        response = await self._http_client.get(url)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        type_adapter = TypeAdapter(tuple[SportActivity, ...])
        return type_adapter.validate_python(response_data['sport_activities'])

    async def do_sports(
            self,
            user_id: int,
            sport_activity_name: str,
    ) -> SportActivityActionResult:
        url = '/sport-activities/'
        request_data = {
            'user_id': user_id,
            'sport_activity_name': sport_activity_name,
        }

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return SportActivityActionResult.model_validate(response_data)
