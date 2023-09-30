__all__ = ('can_create_new_contact', 'compute_new_contact_price')


def can_create_new_contact(*, contact_price: int, balance: int) -> bool:
    return balance >= contact_price


def compute_new_contact_price(contacts_count: int) -> int:
    return 100 * 2 ** contacts_count
