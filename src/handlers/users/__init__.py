from aiogram import Router

from . import update, detail, errors

__all__ = ('router',)

router = Router()

update.register_handlers(router)
detail.register_handlers(router)
router.include_router(errors.router)
