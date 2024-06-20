from pydantic import TypeAdapter

from exceptions import (
    FoodItemDoesNotExistError, InsufficientFundsForWithdrawalError,
    NotEnoughHealthError,
    ServerAPIError,
)
from models import FoodItem, FoodItemConsumptionResult
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

    async def consume(
            self,
            user_id: int,
            food_item_name: str,
    ) -> FoodItemConsumptionResult:
        url = '/food-items/consume/'
        request_data = {'user_id': user_id, 'food_item_name': food_item_name}

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response_data.get('detail') == 'Food item does not exist':
            raise FoodItemDoesNotExistError(
                food_item_name=response_data['food_item_name'],
            )

        if response_data.get('detail') == 'Not enough balance to buy food item':
            raise InsufficientFundsForWithdrawalError(
                amount=int(response_data['price']),
            )

        if response_data.get('detail') == (
                'Not enough health to consume food item'
        ):
            raise NotEnoughHealthError(
                required_health=int(response_data['required_health_value']),
            )

        if response_data.get('ok'):
            return FoodItemConsumptionResult.model_validate(
                response_data['result'],
            )

        raise ServerAPIError
