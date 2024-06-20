from pydantic import TypeAdapter

from exceptions import ServerAPIError
from models import FoodItem
from repositories import APIRepository

__all__ = ('FoodItemRepository',)


class FoodItemRepository(APIRepository):

    async def get_all(self) -> tuple[FoodItem, ...]:
        url = '/food-items/'

        response = await self._http_client.get(url)

        response_data = response.json()

        if response_data.get('ok'):
            type_adapter = TypeAdapter(tuple[FoodItem, ...])
            return type_adapter.validate_python(response_data['result'])

        raise ServerAPIError

    async def consume(self, user_id: int, medicine_name: str):
        url = '/food-items/consume/'
        request_data = {'user_id': user_id, 'food_item_name': medicine_name}

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response_data.get('ok'):
            return

        raise ServerAPIError
