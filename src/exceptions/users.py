from exceptions.base import ApplicationError

__all__ = ('UserDoesNotExistError',)


class UserDoesNotExistError(ApplicationError):

    def __init__(self, detail: str, user_id: int):
        super().__init__(detail)
        self.user_id = user_id
