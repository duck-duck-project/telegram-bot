class MedicineDoesNotExistError(Exception):

    def __init__(self, medicine_name: str):
        super().__init__('Medicine does not exist')
        self.medicine_name = medicine_name
