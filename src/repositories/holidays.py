from models import DateHolidays
from repositories import APIRepository, handle_server_api_errors

__all__ = ('HolidayRepository',)


class HolidayRepository(APIRepository):

    async def get_by_date(self, *, month: int, day: int) -> DateHolidays:
        url = '/holidays/'
        request_query_params = {
            'day': day,
            'month': month
        }
        response = await self._http_client.get(url, params=request_query_params)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return DateHolidays.model_validate(response_data)
