from enum import StrEnum

__all__ = ('ServerApiErrorCode',)


class ServerApiErrorCode(StrEnum):
    CONTACT_DOES_NOT_EXIST = 'CONTACT_DOES_NOT_EXIST'
    CONTACT_ALREADY_EXISTS = 'CONTACT_ALREADY_EXISTS'
