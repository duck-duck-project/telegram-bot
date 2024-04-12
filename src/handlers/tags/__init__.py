from aiogram import Router

from . import create, delete, errors, list, detail

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    create.router,
    delete.router,
    errors.router,
    detail.router,
    list.router,
)
