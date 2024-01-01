from aiogram import Router

from . import private_name, public_name, is_hidden

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    private_name.router,
    public_name.router,
    is_hidden.router,
)
