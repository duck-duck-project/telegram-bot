from collections.abc import Iterable
from datetime import datetime
from zoneinfo import ZoneInfo

from models import ManasId
from services.dates import compute_days_until_birthday, compute_age
from views.base import View

__all__ = ('ClosestBirthdaysView',)


class ClosestBirthdaysView(View):

    def __init__(self, manas_ids: Iterable[ManasId], timezone: ZoneInfo):
        self.__manas_ids = tuple(manas_ids)
        self.__timezone = timezone

    def get_text(self) -> str:
        if not self.__manas_ids:
            return '😔 Нет информации о днях рождений'

        now = datetime.now(tz=self.__timezone).date()

        lines = ['<b>🎉 Ближайшие дни рождения:</b>']

        for manas_id in self.__manas_ids:
            days_until_birthday = compute_days_until_birthday(
                born_at=manas_id.born_at,
                now=now,
            )
            age = compute_age(manas_id.born_at) + 1
            lines.append(
                f'🍭 {manas_id.first_name} - {days_until_birthday} дн.'
                f' (будет {age})'
            )

        return '\n'.join(lines)
