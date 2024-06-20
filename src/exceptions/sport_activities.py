class SportActivitiesThrottledError(Exception):

    def __init__(self, next_sports_in_seconds: int):
        super().__init__('Sports throttled')
        self.next_sports_in_seconds = next_sports_in_seconds


class SportActivityDoesNotExistError(Exception):

    def __init__(self, sport_activity_name: str):
        super().__init__('Sport activity does not exist')
        self.sport_activity_name = sport_activity_name


class SportActivityOnCooldownError(Exception):

    def __init__(self, next_activity_in_seconds: int):
        super().__init__('Sport activity is on cooldown')
        self.next_activity_in_seconds = next_activity_in_seconds
