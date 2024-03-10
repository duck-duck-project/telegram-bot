from aiogram import Router

from . import detail, create, delete

__all__ = ('register_handlers',)


def register_handlers(router: Router) -> None:
    create.register_handlers(router)
    router.include_router(detail.router)
    router.include_router(delete.router)
