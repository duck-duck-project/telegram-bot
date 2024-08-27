class MiningCooldownError(Exception):

    def __init__(self, detail: str, next_mining_in_seconds: int):
        super().__init__(detail)
        self.next_mining_in_seconds = next_mining_in_seconds
