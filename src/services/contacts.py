__all__ = ('can_create_new_contact',)


def can_create_new_contact(
        *,
        contacts_count: int,
        is_premium: bool,
) -> bool:
    return contacts_count < 5 or is_premium
