from aiogram import Router

from . import detail, errors

__all__ = ('router',)

router = Router()

detail.register_handlers(router)
router.include_router(errors.router)
