from aiogram import Router

from . import (
    can_be_added_to_contacts, can_receive_notifications, profile_photo, theme,
    born_on,
)

__all__ = ('register_handlers',)


def register_handlers(router: Router) -> None:
    can_be_added_to_contacts.register_handlers(router)
    can_receive_notifications.register_handlers(router)
    router.include_router(born_on.router)
    router.include_router(theme.router)
    profile_photo.register_handlers(router)
