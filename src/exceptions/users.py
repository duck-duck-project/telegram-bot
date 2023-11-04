from dataclasses import dataclass

__all__ = (
    'UserAlreadyExistsError',
    'UserDoesNotExistError',
    'ThemeDoesNotExistError',
)


@dataclass(frozen=True, slots=True)
class UserDoesNotExistError(Exception):
    user_id: int

    def __str__(self):
        return f'User with Telegram ID {self.user_id} does not exist'


@dataclass(frozen=True, slots=True)
class UserAlreadyExistsError(Exception):
    user_id: int

    def __str__(self):
        return f'User with Telegram ID {self.user_id} already exists'


class ThemeDoesNotExistError(Exception):
    pass
