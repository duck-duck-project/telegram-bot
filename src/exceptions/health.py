class NotEnoughHealthError(Exception):

    def __init__(self, detail: str, required_health_value: int):
        super().__init__(detail)
        self.required_health = required_health_value
