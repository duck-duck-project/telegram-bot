from pydantic import TypeAdapter

from exceptions import ServerAPIError
from models import DailyFoodMenu
from repositories.base import APIRepository

__all__ = ('FoodMenuRepository',)


class FoodMenuRepository(APIRepository):

    async def get_all(self) -> list[DailyFoodMenu]:
        async with self._http_client.get('/food-menu/') as response:
            if response.status != 200:
                raise ServerAPIError
            response_data = await response.json()
        type_adapter = TypeAdapter(list[DailyFoodMenu])
        return type_adapter.validate_python(response_data['food_menus'])
