from datetime import date, datetime

from pydantic import BaseModel

from enums import Course, Gender
from models.departments import Department

__all__ = ('ManasId',)


class ExtraPreference(BaseModel):
    name: str
    value: str


class ManasId(BaseModel):
    user_id: int
    department: Department
    first_name: str
    last_name: str
    patronymic: str | None
    born_at: date
    course: Course
    gender: Gender
    student_id: str | None
    obis_password: str | None
    created_at: datetime
    personality_type: str | None
    document_number: str
    nationality: str | None
    region: str | None
    country: str | None
    extra_preferences: list[ExtraPreference]
