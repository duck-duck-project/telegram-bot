from datetime import date

from pydantic import BaseModel

from enums import Course, Gender
from models.departments import Department

__all__ = ('ManasId',)


class ManasId(BaseModel):
    user_id: int
    department: Department
    first_name: str
    last_name: str
    born_at: date
    course: Course
    gender: Gender
    student_id: str | None
    obis_password: str | None
