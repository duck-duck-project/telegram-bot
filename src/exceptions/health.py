class NotEnoughHealthError(Exception):

    def __init__(self, required_health: int):
        super().__init__('Not enough health')
        self.required_health = required_health
