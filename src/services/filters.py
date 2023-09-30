from collections.abc import Iterable
from typing import Protocol, TypeVar

__all__ = ('filter_not_hidden',)


class HasIsHidden(Protocol):
    is_hidden: bool


HasIsHiddenT = TypeVar('HasIsHiddenT', bound=HasIsHidden)


def filter_not_hidden(items: Iterable[HasIsHiddenT]) -> list[HasIsHiddenT]:
    return [item for item in items if not item.is_hidden]
