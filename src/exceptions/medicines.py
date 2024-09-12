from exceptions.base import ApplicationError

__all__ = ('MedicineDoesNotExistError',)


class MedicineDoesNotExistError(ApplicationError):

    def __init__(self, detail: str, medicine_name: str):
        super().__init__(detail)
        self.medicine_name = medicine_name
