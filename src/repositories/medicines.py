from pydantic import TypeAdapter

from exceptions import ServerAPIError
from models import Medicine
from repositories import APIRepository

__all__ = ('MedicineRepository',)


class MedicineRepository(APIRepository):

    async def get_all(self) -> tuple[Medicine, ...]:
        url = '/medicines/'

        response = await self._http_client.get(url)

        response_data = response.json()

        if response_data.get('ok'):
            type_adapter = TypeAdapter(tuple[Medicine, ...])
            return type_adapter.validate_python(response_data['result'])

        raise ServerAPIError

    async def consume(self, user_id: int, medicine_name: str):
        url = '/medicines/consume/'
        request_data = {'user_id': user_id, 'medicine_name': medicine_name}

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response_data.get('ok'):
            return

        raise ServerAPIError
