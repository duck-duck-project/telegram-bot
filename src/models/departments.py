from pydantic import BaseModel

__all__ = ('Department',)


class Department(BaseModel):
    id: int
    name: str
    code: str
