from exceptions.base import ApplicationError

__all__ = ('NotEnoughEnergyError',)


class NotEnoughEnergyError(ApplicationError):

    def __init__(self, detail: str, required_energy_value: int):
        super().__init__(detail)
        self.required_energy = required_energy_value
