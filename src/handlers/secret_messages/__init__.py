from aiogram import Router

from . import create, direct, errors

__all__ = ('router',)

router = Router(name=__name__)

router.include_router(create.router)
router.include_router(errors.router)
direct.register_handlers(router)
