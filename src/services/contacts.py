__all__ = (
    'can_create_new_contact',
    'compute_new_contact_price',
    'is_user_already_contact',
)

from collections.abc import Iterable

from models import Contact


def can_create_new_contact(*, contact_price: int, balance: int) -> bool:
    return balance >= contact_price


def compute_new_contact_price(contacts_count: int) -> int:
    return 100 * (contacts_count + 1)


def is_user_already_contact(
        *,
        user_id: int,
        contacts: Iterable[Contact],
) -> bool:
    return any(contact.to_user.id == user_id for contact in contacts)
