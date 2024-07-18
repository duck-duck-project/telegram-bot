from aiogram import Router

from . import create, errors

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    errors.router,
    create.router,
)
