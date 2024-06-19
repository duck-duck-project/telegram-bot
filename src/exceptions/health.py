class NotEnoughHealthError(Exception):

    def __init__(self, required_health: int):
        super().__init__('Not enough health')
        self.required_health = required_health


class SportActivitiesThrottledError(Exception):

    def __init__(self, next_sports_in_seconds: int):
        super().__init__('Sports throttled')
        self.next_sports_in_seconds = next_sports_in_seconds
