from aiogram import Router

from . import create

__all__ = ('router',)

router = Router(name=__name__)
router.include_router(create.router)
