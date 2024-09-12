from pydantic import TypeAdapter

from models import DailyFoodMenu
from repositories import handle_server_api_errors
from repositories.base import APIRepository

__all__ = ('FoodMenuRepository',)


class FoodMenuRepository(APIRepository):

    async def get_all(self) -> tuple[DailyFoodMenu, ...]:
        response = await self._http_client.get('/food-menu/')

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        type_adapter = TypeAdapter(tuple[DailyFoodMenu, ...])
        return type_adapter.validate_python(response_data['food_menus'])
