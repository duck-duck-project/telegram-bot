from exceptions.manas_id import ManasIdDoesNotExistError
from models import ManasId
from repositories.base import APIRepository

__all__ = ('ManasIdRepository',)


class ManasIdRepository(APIRepository):

    async def get_manas_id_by_user_id(self, user_id: int) -> ManasId:
        url = f'/manas-id/user-id/{user_id}/'

        async with self._http_client.get(url) as response:
            if response.status == 404:
                raise ManasIdDoesNotExistError(user_id)

            response_data = await response.json()

        return ManasId.model_validate(response_data)
