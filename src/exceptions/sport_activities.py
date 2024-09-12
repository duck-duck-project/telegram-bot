from exceptions.base import ApplicationError

__all__ = (
    'SportActivitiesThrottledError',
    'SportActivityOnCooldownError',
    'SportActivityDoesNotExistError',
)


class SportActivitiesThrottledError(ApplicationError):

    def __init__(self, detail: str, next_sports_in_seconds: int):
        super().__init__(detail)
        self.next_sports_in_seconds = next_sports_in_seconds


class SportActivityDoesNotExistError(ApplicationError):

    def __init__(self, detail: str, sport_activity_name: str):
        super().__init__(detail)
        self.sport_activity_name = sport_activity_name


class SportActivityOnCooldownError(ApplicationError):

    def __init__(self, detail: str, next_activity_in_seconds: int):
        super().__init__(detail)
        self.next_activity_in_seconds = next_activity_in_seconds
