__all__ = (
    'UserDoesNotExistError',
)


class UserDoesNotExistError(Exception):

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__()
