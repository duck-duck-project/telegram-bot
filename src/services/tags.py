from collections.abc import Iterable
from typing import Final

from enums import TagWeight
from exceptions import TagDoesNotExistError
from models import Tag

__all__ = ('TAG_WEIGHT_TO_PRICE', 'find_tag_by_number')

TAG_WEIGHT_TO_PRICE: Final[dict[TagWeight, int]] = {
    TagWeight.GOLD: 1_000_000,
    TagWeight.SILVER: 100_000,
    TagWeight.BRONZE: 10_000,
}


def find_tag_by_number(
        tags: Iterable[Tag],
        tag_number_to_find: int,
) -> Tag:
    for tag_number, tag in enumerate(tags, start=1):
        if tag_number == tag_number_to_find:
            return tag
    raise TagDoesNotExistError(f'Tag number {tag_number_to_find} not found')
