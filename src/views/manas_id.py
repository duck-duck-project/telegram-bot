from aiogram.types import InputFile

from enums import Course, Gender
from models import ManasId
from services.manas_id import generate_manas_id_number
from services.dates import compute_age
from views import PhotoView

__all__ = ('ManasIdView',)


class ManasIdView(PhotoView):

    def __init__(self, manas_id: ManasId, photo: str | InputFile):
        self.__manas_id = manas_id
        self.__photo = photo

    def get_caption(self) -> str:
        course_name = {
            Course.BACHELOR_FIRST: '1 бакалавр',
            Course.BACHELOR_SECOND: '2 бакалавр',
            Course.BACHELOR_THIRD: '3 бакалавр',
            Course.BACHELOR_FOURTH: '4 бакалавр',
            Course.PREPARATION: 'хазырлык',
        }[self.__manas_id.course]
        gender_name = {
            Gender.MALE: 'мужской',
            Gender.FEMALE: 'женский',
        }[self.__manas_id.gender]

        manas_id_number = generate_manas_id_number(self.__manas_id)

        age = compute_age(self.__manas_id.born_at)
        if 1 <= age % 10 <= 4 and age // 10 != 1:
            age_suffix = 'года'
        else:
            age_suffix = 'лет'

        return (
            '<b>🪪 Карточка студента</b>\n'
            '\n'
            '<b>📲 Личная информация:</b>\n'
            f'ФИО: {self.__manas_id.last_name} {self.__manas_id.first_name}\n'
            f'Дата рождения: {self.__manas_id.born_at:%d.%m.%Y}\n'
            f'Возраст: {compute_age(self.__manas_id.born_at)} {age_suffix}\n'
            f'Пол: {gender_name}\n'
            '\n'
            f'<b>🎓 Информация о студенте:</b>\n'
            f'Направление: {self.__manas_id.department.name}\n'
            f'Курс: {course_name}\n'
            '\n'
            f'<b>☁️ Система:</b>\n'
            f'ID номер: {manas_id_number}\n'
            f'Дата выдачи: {self.__manas_id.created_at:%d.%m.%Y}\n'
        )

    def get_photo(self) -> str | InputFile:
        return self.__photo
