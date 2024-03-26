from exceptions import ServerAPIError
from models import DateHolidays
from repositories import APIRepository

__all__ = ('HolidayRepository',)


class HolidayRepository(APIRepository):

    async def get_by_date(self, *, month: int, day: int) -> DateHolidays:
        url = '/holidays/'
        request_query_params = {
            'day': day,
            'month': month
        }
        response = await self._http_client.get(url, params=request_query_params)

        if response.is_success:
            response_data = response.json()

            return DateHolidays.model_validate(response_data['result'])

        raise ServerAPIError
