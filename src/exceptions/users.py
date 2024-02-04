from dataclasses import dataclass

__all__ = (
    'UserAlreadyExistsError',
    'UserDoesNotExistError',
    'ThemeDoesNotExistError',
)


class UserDoesNotExistError(Exception):

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__()


@dataclass(frozen=True, slots=True)
class UserAlreadyExistsError(Exception):
    user_id: int

    def __str__(self):
        return f'User with Telegram ID {self.user_id} already exists'


class ThemeDoesNotExistError(Exception):
    pass
