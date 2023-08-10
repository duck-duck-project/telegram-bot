from django.db.models import QuerySet

from users.exceptions import UserDoesNotExistsError, ContactDoesNotExistError
from users.models import User, Contact

__all__ = (
    'get_user_by_id',
    'get_contact_by_id',
    'get_contacts_by_user_id',
)


def get_user_by_id(user_id: int) -> User:
    """Retrieve user instance by ID.

    Args:
        user_id: Telegram ID of user.

    Returns:
        User instance if exists.

    Raises:
        UserDoesNotExistsError: If user does not exist.
    """
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise UserDoesNotExistsError(user_id=user_id)


def get_contact_by_id(contact_id: int) -> Contact:
    """Retrieve contact instance by ID.

    Args:
        contact_id: ID of contact.

    Returns:
        Contact instance if exists.

    Raises:
        ContactDoesNotExistError: If contact does not exist.
    """
    try:
        return (
            Contact.objects
            .select_related('of_user', 'to_user')
            .get(id=contact_id)
        )
    except Contact.DoesNotExist:
        raise ContactDoesNotExistError(contact_id=contact_id)


def get_contacts_by_user_id(user_id: int) -> QuerySet[Contact]:
    """Retrieve contacts of user.

    Args:
        user_id: ID of user.

    Returns:
        QuerySet of contacts.
    """
    return (
        Contact.objects
        .select_related('of_user', 'to_user')
        .filter(of_user_id=user_id)
    )
