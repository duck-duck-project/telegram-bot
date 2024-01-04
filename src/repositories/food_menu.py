from pydantic import TypeAdapter

from exceptions import ServerAPIError
from models import DailyFoodMenu
from repositories.base import APIRepository

__all__ = ('FoodMenuRepository',)


class FoodMenuRepository(APIRepository):

    async def get_all(self) -> list[DailyFoodMenu]:
        response = await self._http_client.get('/food-menu/')
        if response.status_code != 200:
            raise ServerAPIError
        response_data = response.json()
        type_adapter = TypeAdapter(list[DailyFoodMenu])
        return type_adapter.validate_python(response_data['food_menus'])
