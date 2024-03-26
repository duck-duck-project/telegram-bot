from pydantic import BaseModel

__all__ = ('DateHolidays',)


class DateHolidays(BaseModel):
    day: int
    month: int
    holidays: list[str]
