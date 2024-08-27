from enum import StrEnum, auto

__all__ = ('ServerApiErrorCode',)


class ServerApiErrorCode(StrEnum):
    CONTACT_NOT_FOUND = auto()
    CONTACT_ALREADY_EXISTS = auto()
    SECRET_MEDIA_MESSAGE_NOT_FOUND = auto()
    SECRET_TEXT_MESSAGE_NOT_FOUND = auto()
    MINING_COOLDOWN = auto()
    NOT_ENOUGH_HEALTH = auto()
    NOT_ENOUGH_ENERGY = auto()
