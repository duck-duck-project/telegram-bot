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
