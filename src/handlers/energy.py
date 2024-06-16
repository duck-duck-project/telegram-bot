from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message

from exceptions import NotEnoughEnergyError
from filters.energy import energy_refill_filter
from models import FoodItem
from repositories import BalanceRepository, UserRepository
from services import BalanceNotifier
from services.food import FoodItems, render_energy
from views import EnergyRefillView, FoodItemsListView, reply_view

__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(NotEnoughEnergyError))
async def on_not_enough_energy_error(
        event: ErrorEvent,
) -> None:
    exception: NotEnoughEnergyError = event.exception
    await event.update.message.reply(
        f'🪫 Необходимо {render_energy(exception.required_energy)}'
        ' энергии для этого действия.\n'
        '📲 Используйте <code>ID</code> чтобы посмотреть свою энергию'
        'Посмотреть список еды можно командой <code>еда список</code>'
    )


@router.message(
    energy_refill_filter,
    StateFilter('*'),
)
async def on_energy_refill(
        message: Message,
        user_repository: UserRepository,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
        food_item: FoodItem,
) -> None:
    withdrawal = await balance_repository.create_withdrawal(
        user_id=message.from_user.id,
        amount=food_item.price,
        description=f'{food_item.emoji} Покупка "{food_item.name}"',
    )
    await balance_notifier.send_withdrawal_notification(withdrawal)
    user_energy_refill = await user_repository.refill_energy(
        user_id=message.from_user.id,
        energy=food_item.energy,
    )
    view = EnergyRefillView(
        user_energy_refill=user_energy_refill,
        food_item=food_item,
    )
    await reply_view(message=message, view=view)


@router.message(
    F.text.lower() == 'еда список',
    StateFilter('*'),
)
async def on_food_items_list(message: Message, food_items: FoodItems) -> None:
    view = FoodItemsListView(food_items)
    await reply_view(message=message, view=view)
