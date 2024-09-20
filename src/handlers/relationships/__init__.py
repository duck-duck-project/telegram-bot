from aiogram import Router

from . import offer

__all__ = ('router',)

router = Router(name=__name__)
router.include_router(create.router)
