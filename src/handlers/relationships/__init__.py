from aiogram import Router

from . import accept_offer, break_up, create_offer, detail, errors

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    errors.router,
    create_offer.router,
    accept_offer.router,
    detail.router,
    break_up.router,
)
