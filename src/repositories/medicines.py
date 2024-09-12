from pydantic import TypeAdapter

from models import Medicine, MedicineConsumptionResult
from repositories import APIRepository, handle_server_api_errors

__all__ = ('MedicineRepository',)


class MedicineRepository(APIRepository):

    async def get_all(self) -> tuple[Medicine, ...]:
        url = '/medicines/'

        response = await self._http_client.get(url)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        type_adapter = TypeAdapter(tuple[Medicine, ...])
        return type_adapter.validate_python(response_data['medicines'])

    async def consume(
            self,
            user_id: int,
            medicine_name: str,
    ) -> MedicineConsumptionResult:
        url = '/medicines/consume/'
        request_data = {'user_id': user_id, 'medicine_name': medicine_name}

        response = await self._http_client.post(url, json=request_data)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return MedicineConsumptionResult.model_validate(response_data)
