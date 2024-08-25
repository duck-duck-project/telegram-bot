from typing import Generic, TypeVar

from pydantic import BaseModel

__all__ = ('ServerResponse',)

T = TypeVar('T')


class ServerResponse(BaseModel, Generic[T]):
    ok: bool
    result: T | None = None
    error: str | None = None
