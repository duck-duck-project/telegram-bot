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
    USER_NOT_FOUND = auto()
    INSUFFICIENT_FUNDS = auto()
    TAG_NOT_FOUND = auto()
    WISH_NOT_FOUND = auto()
    PREDICTION_NOT_FOUND = auto()
    TRUTH_OR_DARE_QUESTION_NOT_FOUND = auto()
    SPORT_ACTIVITY_COOLDOWN = auto()
    MEDICINE_NOT_FOUND = auto()
    SECRET_TEXT_MESSAGE_ID_CONFLICT = auto()
    FOOD_ITEM_NOT_FOUND = auto()
    SPORT_ACTIVITY_NOT_FOUND = auto()
