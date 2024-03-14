from aiogram import Router

from . import create, delete, detail

__all__ = ('register_handlers',)


def register_handlers(router: Router) -> None:
    router.include_routers(
        create.router,
        detail.router,
        delete.router,
    )
