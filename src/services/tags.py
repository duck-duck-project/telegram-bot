from collections.abc import Iterable
from typing import Final

from enums import TagWeight
from exceptions import TagDoesNotExistError
from models import Tag

__all__ = (
    'TAG_WEIGHT_TO_PRICE',
    'find_tag_by_number',
    'compute_tag_refund_price',
    'compute_tag_issue_price',
)

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


def compute_tag_refund_price(
        *,
        tag_weight: TagWeight,
        is_premium: bool,
) -> int:
    coefficient = 0.75 if is_premium else 0.5
    return int(TAG_WEIGHT_TO_PRICE[tag_weight] * coefficient)


def compute_tag_issue_price(
        *,
        tag_weight: TagWeight,
        is_premium: bool,
) -> int:
    coefficient = 0.75 if is_premium else 1
    return int(TAG_WEIGHT_TO_PRICE[tag_weight] * coefficient)
