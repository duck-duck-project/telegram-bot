from enum import IntEnum

__all__ = ('ContactsSortingStrategy',)


class ContactsSortingStrategy(IntEnum):
    CREATION_TIME = 1
    PUBLIC_NAME = 2
    PRIVATE_NAME = 3
