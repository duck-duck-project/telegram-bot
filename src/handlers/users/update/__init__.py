from aiogram import Router

from . import profile_photo

__all__ = ('register_handlers',)


def register_handlers(router: Router) -> None:
    profile_photo.register_handlers(router)
