from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message

from enums import FoodItemType
from exceptions import FoodItemDoesNotExistError, NotEnoughEnergyError
from filters.energy import food_item_filter
from repositories import FoodItemRepository
from services import render_units
from services.clean_up import CleanUpService
from views import FoodItemConsumedView, FoodItemsListView, reply_view

__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(FoodItemDoesNotExistError))
async def on_food_item_does_not_exist_error(event: ErrorEvent) -> None:
    # noinspection PyTypeChecker
    exception: FoodItemDoesNotExistError = event.exception
    await event.update.message.reply(
        '🚫 Блюда или напитка с названием'
        f' <code>{exception.food_item_name}</code> не существует\n'
        '📲 Используйте <code>еда список</code>'
        ' чтобы посмотреть список доступной еды\n'
    )


@router.error(ExceptionTypeFilter(NotEnoughEnergyError))
async def on_not_enough_energy_error(
        event: ErrorEvent,
) -> None:
    # noinspection PyTypeChecker
    exception: NotEnoughEnergyError = event.exception
    await event.update.message.reply(
        f'🪫 Необходимо {render_units(exception.required_energy)}'
        ' энергии для этого действия.\n'
        '📲 Используйте <code>ID</code> чтобы посмотреть свою энергию\n'
        '\n'
        'Используйте команду <code>еда список</code>'
        ' чтобы посмотреть список доступной еды\n'
    )


@router.message(
    food_item_filter,
    StateFilter('*'),
)
async def on_energy_refill(
        message: Message,
        food_item_type: FoodItemType,
        food_item_name: str,
        food_item_repository: FoodItemRepository,
        clean_up_service: CleanUpService,
) -> None:
    food_item_consumption_result = await food_item_repository.consume(
        user_id=message.from_user.id,
        food_item_name=food_item_name,
    )
    view = FoodItemConsumedView(
        food_item_consumption_result=food_item_consumption_result,
        food_item_type=food_item_type,
    )
    sent_message = await reply_view(message=message, view=view)
    await clean_up_service.create_clean_up_task(message, sent_message)


@router.message(
    F.text.lower() == 'еда список',
    StateFilter('*'),
)
async def on_food_items_list(
        message: Message,
        food_item_repository: FoodItemRepository,
        clean_up_service: CleanUpService,
) -> None:
    food_items = await food_item_repository.get_all()
    view = FoodItemsListView(food_items)
    sent_message = await reply_view(message=message, view=view)
    await clean_up_service.create_clean_up_task(message, sent_message)

