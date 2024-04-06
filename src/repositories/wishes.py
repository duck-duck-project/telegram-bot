from repositories import APIRepository

__all__ = ('WishRepository',)


class WishRepository(APIRepository):

    async def get_random(self) -> str | None:
        response = await self._http_client.get('/wishes/random/')

        if response.is_success:
            return response.json()['text']

        return None
