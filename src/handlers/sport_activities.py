from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter, StateFilter
from aiogram.types import ErrorEvent, Message

from exceptions import (
    NotEnoughHealthError, SportActivitiesThrottledError,
    SportActivityDoesNotExistError, SportActivityOnCooldownError,
)
from filters import sport_activity_filter
from repositories import SportActivityRepository
from views import (
    NotEnoughHealthView,
    SportActivitiesListView,
    SportActivitiesThrottledView,
    SportActivityDoneView,
    reply_view,
)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(SportActivityDoesNotExistError))
async def on_sport_activity_does_not_exist_error(event: ErrorEvent) -> None:
    # noinspection PyTypeChecker
    exception: SportActivityDoesNotExistError = event.exception
    await event.update.message.reply(
        f'❌ Упражнение <b>{exception.sport_activity_name}</b> не существует'
    )


@router.error(ExceptionTypeFilter(SportActivityOnCooldownError))
async def on_sport_activity_on_cooldown_error(event: ErrorEvent) -> None:
    # noinspection PyTypeChecker
    exception: SportActivityOnCooldownError = event.exception
    view = SportActivitiesThrottledView(exception.next_activity_in_seconds)
    await reply_view(message=event.update.message, view=view)


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
        sport_activity_repository: SportActivityRepository,
        sport_activity_name: str
) -> None:
    sport_activity_action_result = await sport_activity_repository.do_sports(
        user_id=message.from_user.id,
        sport_activity_name=sport_activity_name,
    )
    view = SportActivityDoneView(sport_activity_action_result)
    await reply_view(message=message, view=view)


@router.message(
    F.text.lower().startswith('заняться спортом'),
    StateFilter('*'),
)
async def on_show_sport_activities_list(
        message: Message,
        sport_activity_repository: SportActivityRepository,
) -> None:
    sport_activities = await sport_activity_repository.get_all()
    view = SportActivitiesListView(sport_activities)
    await reply_view(message=message, view=view)
