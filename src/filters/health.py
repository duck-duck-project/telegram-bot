from aiogram.types import Message

from services import SportActivities

__all__ = ('sport_activity_filter',)


def sport_activity_filter(
        message: Message,
        sport_activities: SportActivities,
) -> bool | dict:
    if message.text is None:
        return False

    if not message.text.lower().startswith('заняться спортом '):
        return False

    activity_name = message.text[16:].strip()

    sport_activity = sport_activities.find_by_name(activity_name)

    if sport_activity is None:
        return False

    return {'sport_activity': sport_activity}
