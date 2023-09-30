from typing import Iterable
from uuid import UUID

from exceptions import InvalidSecretMediaDeeplinkError
from models import Contact, HasUserId

__all__ = (
    'can_see_team_secret',
    'can_see_contact_secret',
    'extract_secret_media_id',
)


def can_see_team_secret(
        *,
        user_id: int,
        team_members: Iterable[HasUserId],
) -> bool:
    user_ids = {member.user_id for member in team_members}
    return user_id in user_ids


def can_see_contact_secret(
        *,
        user_id: int,
        contact: Contact,
) -> bool:
    return user_id in (
        contact.of_user.id,
        contact.to_user.id,
    )


def extract_secret_media_id(deep_link: str) -> UUID:
    try:
        return UUID(deep_link.split('-')[-1])
    except (ValueError, IndexError):
        raise InvalidSecretMediaDeeplinkError
