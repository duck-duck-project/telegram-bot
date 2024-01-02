from enums import Course, Gender
from models import ManasId
from services.dates import compute_age
from views.base import View

__all__ = ('ManasIdView',)


class ManasIdView(View):

    def __init__(self, manas_id: ManasId):
        self.__manas_id = manas_id

    def get_text(self) -> str:
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

        age = compute_age(self.__manas_id.born_at)
        if 2 <= age % 10 <= 4 and age // 10 != 1:
            age_suffix = 'года'
        else:
            age_suffix = 'лет'

        return (
            f'<b>🪪 Карточка студента</b>\n'
            f'ФИО: {self.__manas_id.last_name} {self.__manas_id.first_name}\n'
            f'Возраст: {compute_age(self.__manas_id.born_at)} {age_suffix}\n'
            f'Пол: {gender_name}\n'
            f'Направление: {self.__manas_id.department.name}\n'
            f'Курс: {course_name}'
        )
