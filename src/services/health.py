import pathlib
from collections.abc import Iterable

from pydantic import TypeAdapter

from models import SportActivity

__all__ = ('SportActivities', 'load_sport_activities')


def load_sport_activities(file_path: pathlib.Path) -> tuple[SportActivity, ...]:
    sport_activities_json = file_path.read_text(encoding='utf-8')
    type_adapter = TypeAdapter(tuple[SportActivity, ...])
    return type_adapter.validate_json(sport_activities_json)


class SportActivities:

    def __init__(self, sport_activities: Iterable[SportActivity]):
        self.__sport_activities = tuple(sport_activities)

    def find_by_name(self, name: str) -> SportActivity | None:
        for sport_activity in self.__sport_activities:
            if sport_activity.name.lower() == name.lower().strip():
                return sport_activity

    def __iter__(self):
        return iter(self.__sport_activities)
