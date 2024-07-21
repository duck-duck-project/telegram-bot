from aiogram import Router

from . import (
    profile_photo,
    theme,
)

__all__ = ('register_handlers',)


def register_handlers(router: Router) -> None:
    router.include_router(theme.router)
    profile_photo.register_handlers(router)
