from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message, User as TelegramUser

from enums import FoodItemType
from exceptions import FoodItemDoesNotExistError, NotEnoughEnergyError
from filters.energy import feed_other_user_filter, feed_self_filter
from repositories import FoodItemRepository
from services import render_units
from services.clean_up import CleanUpService
from views import (
    FeedOtherUserView, FeedSelfView, FoodItemsListView, answer_view, reply_view,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(FoodItemDoesNotExistError))
async def on_food_item_does_not_exist_error(event: ErrorEvent) -> None:
    # noinspection PyTypeChecker
    exception: FoodItemDoesNotExistError = event.exception
    await event.update.message.reply(
        '🚫 Блюда или напитка с названием'
        f' <code>{exception.food_item_name}</code> не существует\n'
        '📲 Используйте <code>список еды</code>'
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
        'Используйте команду <code>список еды</code>'
        ' чтобы посмотреть список доступной еды\n'
    )


@router.message(
    feed_self_filter,
    StateFilter('*'),
)
async def on_feed_self(
        message: Message,
        food_item_type: FoodItemType,
        food_item_name: str,
        food_item_repository: FoodItemRepository,
        clean_up_service: CleanUpService,
) -> None:
    food_item_consumption_result = await food_item_repository.feed(
        from_user_id=message.from_user.id,
        to_user_id=message.from_user.id,
        food_item_name=food_item_name,
    )
    view = FeedSelfView(
        food_item_consumption_result=food_item_consumption_result,
        food_item_type=food_item_type,
    )
    sent_message = await reply_view(message=message, view=view)
    await clean_up_service.create_clean_up_task(message, sent_message)


@router.message(
    feed_other_user_filter,
    StateFilter('*'),
)
async def on_feed_other_user(
        message: Message,
        food_item_type: FoodItemType,
        food_item_name: str,
        food_item_repository: FoodItemRepository,
        clean_up_service: CleanUpService,
        from_user: TelegramUser,
        to_user: TelegramUser,
) -> None:
    food_item_consumption_result = await food_item_repository.feed(
        from_user_id=from_user.id,
        to_user_id=to_user.id,
        food_item_name=food_item_name,
    )
    view = FeedOtherUserView(
        food_item_consumption_result=food_item_consumption_result,
        food_item_type=food_item_type,
        from_user=from_user,
        to_user=to_user,
    )
    sent_message = await answer_view(message=message, view=view)
    await clean_up_service.create_clean_up_task(message, sent_message)


@router.message(
    F.text.lower().in_({
        'еда список',
        'еда',
        'меню',
        'список еды',
        'покушать',
        'поесть',
        'попить',
    }),
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
