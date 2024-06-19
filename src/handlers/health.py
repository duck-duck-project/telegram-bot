from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message

from exceptions import NotEnoughHealthError, SportActivitiesThrottledError
from filters import sport_activity_filter
from models import SportActivity
from repositories import UserRepository
from services import SportActivities
from views import (
    NotEnoughHealthView, SportActivitiesListView, SportActivitiesThrottledView,
    SportActivityDoneView, reply_view,
)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(NotEnoughHealthError))
async def on_not_enough_health_error(event: ErrorEvent) -> None:
    # noinspection PyTypeChecker
    exception: NotEnoughHealthError = event.exception
    view = NotEnoughHealthView(exception.required_health)
    await reply_view(message=event.update.message, view=view)


@router.error(ExceptionTypeFilter(SportActivitiesThrottledError))
async def on_sport_activities_throttled_error(event: ErrorEvent) -> None:
    # noinspection PyTypeChecker
    exception: SportActivitiesThrottledError = event.exception
    view = SportActivitiesThrottledView(exception.next_sports_in_seconds)
    await reply_view(message=event.update.message, view=view)


@router.message(
    sport_activity_filter,
    StateFilter('*'),
)
async def on_do_sports(
        message: Message,
        user_repository: UserRepository,
        sport_activity: SportActivity,
) -> None:
    sports_result = await user_repository.do_sports(
        user_id=message.from_user.id,
        energy_cost_value=sport_activity.energy_cost_value,
        health_benefit_value=sport_activity.health_benefit_value,
    )
    view = SportActivityDoneView(
        sport_activity=sport_activity,
        current_health=sports_result.health,
    )
    await reply_view(message=message, view=view)


@router.message(
    F.text.lower().startswith('заняться спортом'),
    StateFilter('*'),
)
async def on_show_sport_activities_list(
        message: Message,
        sport_activities: SportActivities,
) -> None:
    view = SportActivitiesListView(sport_activities)
    await reply_view(message=message, view=view)
