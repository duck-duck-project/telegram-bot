from aiogram import Router

from . import (
    born_on,
    can_be_added_to_contacts,
    can_receive_notifications,
    personality_type,
    profile_photo,
    theme,
)

__all__ = ('register_handlers',)


def register_handlers(router: Router) -> None:
    can_be_added_to_contacts.register_handlers(router)
    can_receive_notifications.register_handlers(router)
    router.include_router(born_on.router)
    router.include_router(theme.router)
    router.include_router(personality_type.router)
    profile_photo.register_handlers(router)
