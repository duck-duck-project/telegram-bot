from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import CallbackQuery, Message

from callback_data import FoodMenuDetailCallbackData
from filters import (
    food_menu_for_n_days_filter, food_menu_for_today_filter,
    food_menu_for_tomorrow_filter,
)
from repositories import FoodMenuRepository
from services.clean_up import CleanUpService
from views import (
    FoodMenuFAQView, FoodMenuMediaGroupView, answer_media_group_view,
    answer_view,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    FoodMenuDetailCallbackData.filter(),
    StateFilter('*'),
)
async def on_show_food_menu_for_specific_day_callback(
        callback_query: CallbackQuery,
        callback_data: FoodMenuDetailCallbackData,
        food_menu_repository: FoodMenuRepository,
        clean_up_service: CleanUpService,
) -> None:
    food_menus = await food_menu_repository.get_all()

    try:
        food_menu = food_menus[callback_data.days_skip_count]
    except IndexError:
        await callback_query.answer(
            text='❌ Нет данных о меню на указанный день',
            show_alert=True,
        )
    else:
        view = FoodMenuMediaGroupView(food_menu)
        messages = await answer_media_group_view(
            message=callback_query.message,
            view=view,
        )
        await clean_up_service.create_clean_up_task(*messages)
    finally:
        await callback_query.message.delete()


@router.message(
    F.content_type == ContentType.TEXT,
    or_f(
        food_menu_for_today_filter,
        food_menu_for_tomorrow_filter,
        food_menu_for_n_days_filter,
    ),
    StateFilter('*'),
)
async def on_show_food_menu_for_specific_day(
        message: Message,
        food_menu_repository: FoodMenuRepository,
        days_skip_count: int,
        clean_up_service: CleanUpService,
) -> None:
    food_menus = await food_menu_repository.get_all()

    try:
        food_menu = food_menus[days_skip_count]
    except IndexError:
        await message.reply('❌ Нет данных о меню на указанный день')
        return

    view = FoodMenuMediaGroupView(food_menu)
    messages = await answer_media_group_view(message=message, view=view)
    await clean_up_service.create_clean_up_task(message, *messages)


@router.message(
    F.content_type == ContentType.TEXT,
    or_f(
        Command('yemek'),
        F.text == '🍽️ Йемек',
    ),
    StateFilter('*'),
)
async def on_show_food_menu_instructions(
    message: Message,
    clean_up_service: CleanUpService,
) -> None:
    await answer_view(message=message, view=FoodMenuFAQView())
    await clean_up_service.create_clean_up_task(message)
