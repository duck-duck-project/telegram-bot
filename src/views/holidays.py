import random

from models import DateHolidays
from views.base import View

__all__ = ('HolidayView',)


class HolidayView(View):

    def __init__(self, date_holidays: DateHolidays):
        self.__date_holidays = date_holidays

    def get_text(self) -> str:
        if not self.__date_holidays.holidays:
            return '😔 Нет данных по праздникам на сегодня'
        holiday = random.choice(self.__date_holidays.holidays)
        return f'<b>ℹ️ Праздник сегодня:</b>\n{holiday}'
