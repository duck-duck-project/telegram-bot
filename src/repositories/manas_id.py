from pydantic import TypeAdapter

from exceptions.manas_id import ManasIdDoesNotExistError
from models import ManasId
from repositories.base import APIRepository

__all__ = ('ManasIdRepository',)


class ManasIdRepository(APIRepository):

    async def get_manas_id_by_user_id(self, user_id: int) -> ManasId:
        url = f'/manas-id/user-id/{user_id}/'

        response = await self._http_client.get(url)
        if response.status_code == 404:
            raise ManasIdDoesNotExistError(user_id)

        response_data = response.json()
        return ManasId.model_validate(response_data)

    async def get_all(
            self,
            *,
            limit: int | None = 100,
            offset: int | None = 0,
    ) -> list[ManasId]:
        url = '/manas-id/'

        manas_ids: list[ManasId] = []
        while True:
            request_query_params = {
                'limit': limit,
                'offset': offset,
            }
            response = await self._http_client.get(
                url=url,
                params=request_query_params,
            )
            response_data = response.json()

            manas_ids += response_data['result']['manas_ids']

            if response_data['result']['is_end_of_list_reached']:
                break

            offset += limit

        type_adapter = TypeAdapter(list[ManasId])
        return type_adapter.validate_python(manas_ids)
