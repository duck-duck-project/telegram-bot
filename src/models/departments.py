from pydantic import BaseModel

__all__ = ('Department',)


class Department(BaseModel):
    id: int
    name: str
    emoji: str | None
    code: str | None
