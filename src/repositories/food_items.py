from pydantic import TypeAdapter

from enums import FoodItemType
from models import FoodItem, FoodItemFeedResult
from repositories import APIRepository, handle_server_api_errors

__all__ = ('FoodItemRepository',)


class FoodItemRepository(APIRepository):

    async def get_all(self) -> tuple[FoodItem, ...]:
        url = '/food-items/'

        response = await self._http_client.get(url)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        type_adapter = TypeAdapter(tuple[FoodItem, ...])
        return type_adapter.validate_python(response_data['food_items'])

    async def feed(
            self,
            from_user_id: int,
            to_user_id: int,
            food_item_name: str,
            food_item_type: FoodItemType,
    ) -> FoodItemFeedResult:
        url = '/food-items/feed/'
        request_data = {
            'from_user_id': from_user_id,
            'to_user_id': to_user_id,
            'food_item_name': food_item_name,
            'food_item_type': food_item_type,
        }

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return FoodItemFeedResult.model_validate(response_data)
