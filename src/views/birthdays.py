from collections.abc import Iterable
from datetime import datetime
from zoneinfo import ZoneInfo

from models import ContactBirthday
from services.users import get_username_or_fullname
from services.dates import compute_age, compute_days_until_birthday
from views.base import View

__all__ = ('BirthdayListView',)


class BirthdayListView(View):

    def __init__(
            self,
            contacts: Iterable[ContactBirthday],
            timezone: ZoneInfo,
    ):
        self.__contacts = tuple(contacts)
        self.__timezone = timezone

    def get_text(self) -> str:
        if not self.__contacts:
            return '😔 Нет информации о днях рождений ваших контактов'

        now = datetime.now(tz=self.__timezone).date()

        lines = ['<b>🎉 Ближайшие дни рождения ваших контактов:</b>']

        contacts_and_days_until_birthday = [
            (
                contact,
                compute_days_until_birthday(
                    born_at=contact.born_on,
                    now=now,
                )
            )
            for contact in self.__contacts
        ]

        contacts_and_days_until_birthday = sorted(
            contacts_and_days_until_birthday,
            key=lambda item: item[1],
        )

        for contact, days_until_birthday in contacts_and_days_until_birthday:
            age = compute_age(contact.born_on)
            name = get_username_or_fullname(contact.user)

            if days_until_birthday == 0:
                days_until_birthday = '🔥 Сегодня'
            elif days_until_birthday == 1:
                days_until_birthday = '🙌 Завтра'
                age += 1
            else:
                days_until_birthday = f'{days_until_birthday} дн.'
                age += 1
            lines.append(
                f'🍭 {name} - {days_until_birthday}'
                f' ({age})'
            )

        return '\n'.join(lines)
