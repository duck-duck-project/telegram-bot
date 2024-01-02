from dataclasses import dataclass

__all__ = ('ManasIdDoesNotExistError',)


@dataclass(frozen=True, slots=True)
class ManasIdDoesNotExistError(Exception):
    user_id: int

    def __str__(self):
        return f'ManasId with {self.user_id=} does not exist'
