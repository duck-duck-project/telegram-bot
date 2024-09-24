from datetime import datetime

from pydantic import BaseModel

from models.users import UserPartial

__all__ = (
    'RelationshipCreateResult',
    'Relationship',
    'RelationshipBreakUpResult',
)


class RelationshipCreateResult(BaseModel):
    id: int
    first_user: UserPartial
    second_user: UserPartial
    created_at: datetime


class Relationship(BaseModel):
    id: int
    first_user: UserPartial
    second_user: UserPartial
    created_at: datetime
    level: int
    experience: int
    next_level_experience_threshold: int


class RelationshipBreakUpResult(BaseModel):
    first_user: UserPartial
    second_user: UserPartial
    created_at: datetime
    broke_up_at: datetime
    level: int
