from collections.abc import Iterable
from datetime import datetime
from zoneinfo import ZoneInfo

from services.dates import compute_days_until_birthday, compute_age
from views.base import View

__all__ = ('ClosestBirthdaysView',)


class ClosestBirthdaysView(View):

    def __init__(self, manas_ids: Iterable, timezone: ZoneInfo):
        self.__manas_ids = tuple(manas_ids)
        self.__timezone = timezone

    def get_text(self) -> str:
        if not self.__manas_ids:
            return '😔 Нет информации о днях рождений'

        now = datetime.now(tz=self.__timezone).date()

        lines = ['<b>🎉 Ближайшие дни рождения:</b>']

        for manas_id in sorted(self.__manas_ids, key=lambda manas_id: compute_days_until_birthday(
            now=now,
            born_at=manas_id.born_at,
        )):
            days_until_birthday = compute_days_until_birthday(
                born_at=manas_id.born_at,
                now=now,
            )
            age = compute_age(manas_id.born_at)
            if days_until_birthday == 0:
                days_until_birthday = '🔥 Сегодня'
            elif days_until_birthday == 1:
                days_until_birthday = '🙌 Завтра'
                age += 1
            else:
                days_until_birthday = f'{days_until_birthday} дн.'
                age += 1
            lines.append(
                f'🍭 {manas_id.first_name} - {days_until_birthday}'
                f' ({age})'
            )

        return '\n'.join(lines)
