from aiogram import Router

from . import delete, list, create, detail, update, errors

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    errors.router,
    delete.router,
    list.router,
    create.router,
    detail.router,
    update.router,
)
