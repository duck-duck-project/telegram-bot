class NotEnoughEnergyError(Exception):

    def __init__(self, required_energy: int):
        super().__init__('Not enough energy')
        self.required_energy = required_energy
