from aiogram import Router

from . import (
    personality_type,
    profile_photo,
    theme,
)

__all__ = ('register_handlers',)


def register_handlers(router: Router) -> None:
    router.include_router(theme.router)
    router.include_router(personality_type.router)
    profile_photo.register_handlers(router)
