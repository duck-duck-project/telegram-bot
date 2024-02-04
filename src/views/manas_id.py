from collections.abc import Iterable

from aiogram.types import InputMediaPhoto

from enums import Course, Gender
from models import ManasId
from services.dates import compute_age
from services.manas_id import (
    humanize_personality_type,
    determine_zodiac_sign,
    compute_living_days,
)
from views import MediaGroupView

__all__ = ('ManasIdView',)


class ManasIdView(MediaGroupView):

    def __init__(self, manas_id: ManasId, photos: Iterable[str]):
        self.__manas_id = manas_id
        self.__photos = tuple(photos)

    def get_caption(self) -> str:
        course_name = {
            Course.BACHELOR_FIRST: '1 бакалавр',
            Course.BACHELOR_SECOND: '2 бакалавр',
            Course.BACHELOR_THIRD: '3 бакалавр',
            Course.BACHELOR_FOURTH: '4 бакалавр',
            Course.PREPARATION: 'хазырлык',
            Course.APPLICANT: 'абитуриент',
        }[self.__manas_id.course]
        gender_name = {
            Gender.MALE: 'мужской',
            Gender.FEMALE: 'женский',
        }[self.__manas_id.gender]

        age = compute_age(self.__manas_id.born_at)
        if 4 >= age % 10 >= 1 != age // 10:
            age_suffix = 'года'
        else:
            age_suffix = 'лет'

        personality_type = humanize_personality_type(
            personality_type=self.__manas_id.personality_type,
        )
        zodiac_sign = determine_zodiac_sign(
            month=self.__manas_id.born_at.month,
            day=self.__manas_id.born_at.day,
        )
        full_name = f'{self.__manas_id.last_name} {self.__manas_id.first_name}'
        if self.__manas_id.patronymic is not None:
            full_name = f'{full_name} {self.__manas_id.patronymic}'

        country = self.__manas_id.country or 'не определено'
        region = self.__manas_id.region or 'не определено'
        nationality = self.__manas_id.nationality or 'не определено'

        living_days = compute_living_days(self.__manas_id.born_at)

        lines = [
            '<b>🪪 Карточка студента</b>\n',
            '<b>📲 Личная информация:</b>',
            f'ФИО: {full_name}',
            f'Дата рождения: {self.__manas_id.born_at:%d.%m.%Y}',
            f'Возраст: {compute_age(self.__manas_id.born_at)} {age_suffix}',
            f'Живёт на Земле: {living_days} дней',
            f'Пол: {gender_name}',
            f'Страна: {country}',
            f'Регион: {region}',
            f'Национальность: {nationality}',
            '\n'
            f'<b>🎓 Информация о студенте:</b>',
            f'Направление: {self.__manas_id.department.name}',
            f'Курс: {course_name}\n',
            f'<b>☁️ Система:</b>',
            f'ID номер: {self.__manas_id.document_number}',
            f'Дата выдачи: {self.__manas_id.created_at:%d.%m.%Y}\n',
            f'<b>✏️ Прочее:</b>',
            f'Тип личности: {personality_type}',
            f'Знак зодиака: {zodiac_sign}',
        ]

        if self.__manas_id.extra_preferences:
            lines.append('\n<b>✨ Дополнительная информация:</b>')
            for preference in self.__manas_id.extra_preferences:
                lines.append(f'{preference.name}: {preference.value}')

        return '\n'.join(lines)

    def get_medias(self) -> list[InputMediaPhoto]:
        return [
            InputMediaPhoto(media=photo_file_id)
            for photo_file_id in self.__photos
        ]
