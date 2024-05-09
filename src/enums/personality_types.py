from enum import StrEnum

__all__ = ('PersonalityTypeSuffix', 'PersonalityTypePrefix')


class PersonalityTypeSuffix(StrEnum):
    ASSERTIVE = 'A', 'Assertive'
    TURBULENT = 'T', 'Turbulent'


class PersonalityTypePrefix(StrEnum):
    ARCHITECT = 'INTJ', 'Стратег (INTJ)'
    LOGICIAN = 'INTP', 'Ученый (INTP)'
    COMMANDER = 'ENTJ', 'Командир (ENTJ)'
    DEBATER = 'ENTP', 'Полемист (ENTP)'
    ADVOCATE = 'INFJ', 'Активист (INFJ)'
    MEDIATOR = 'INFP', 'Посредник (INFP)'
    PROTAGONIST = 'ENFJ', 'Тренер (ENFJ)'
    CAMPAIGNER = 'ENFP', 'Борец (ENFP)'
    LOGISTICIAN = 'ISTJ', 'Администратор (ISTJ)'
    DEFENDER = 'ISFJ', 'Защитник (ISFJ)'
    EXECUTIVE = 'ESTJ', 'Менеджер (ESTJ)'
    CONSUL = 'ESFJ', 'Консул (ESFJ)'
    VIRTUOSO = 'ISTP', 'Виртуоз (ISTP)'
    ADVENTURER = 'ISFP', 'Артист (ISFP)'
    ENTREPRENEUR = 'ESTP', 'Делец (ESTP)'
    ENTERTAINER = 'ESFP', 'Развлекатель (ESFP)'
