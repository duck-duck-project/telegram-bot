from enum import StrEnum

__all__ = ('PersonalityTypeSuffix', 'PersonalityTypePrefix')


class PersonalityTypeSuffix(StrEnum):
    ASSERTIVE = 'A'
    TURBULENT = 'T'


class PersonalityTypePrefix(StrEnum):
    ARCHITECT = 'INTJ'
    LOGICIAN = 'INTP'
    COMMANDER = 'ENTJ'
    DEBATER = 'ENTP'
    ADVOCATE = 'INFJ'
    MEDIATOR = 'INFP'
    PROTAGONIST = 'ENFJ'
    CAMPAIGNER = 'ENFP'
    LOGISTICIAN = 'ISTJ'
    DEFENDER = 'ISFJ'
    EXECUTIVE = 'ESTJ'
    CONSUL = 'ESFJ'
    VIRTUOSO = 'ISTP'
    ADVENTURER = 'ISFP'
    ENTREPRENEUR = 'ESTP'
    ENTERTAINER = 'ESFP'
