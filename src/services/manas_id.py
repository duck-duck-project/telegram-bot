__all__ = (
    'humanize_personality_type',
    'determine_zodiac_sign',
)


def humanize_personality_type(personality_type: str | None) -> str:
    if personality_type is None:
        return 'Неопределено'

    personality_type_main = personality_type.upper().split('-')[0]

    personality_type_to_name = {
        'INTJ': 'Стратег',
        'INTP': 'Ученый',
        'ENTJ': 'Командир',
        'ENTP': 'Полемист',
        'INFJ': 'Активист',
        'INFP': 'Посредник',
        'ENFJ': 'Тренер',
        'ENFP': 'Борец',
        'ISTJ': 'Администратор',
        'ISFJ': 'Защитник',
        'ESTJ': 'Менеджер',
        'ESFJ': 'Консул',
        'ISTP': 'Виртуоз',
        'ISFP': 'Артист',
        'ESTP': 'Делец',
        'ESFP': 'Развлекатель',
    }

    try:
        name = personality_type_to_name[personality_type_main]
    except KeyError:
        return 'Неопределено'

    return (
        f'{name} (<a href="https://www.16personalities.com/ru/lichnost-'
        f'{personality_type_main.lower()}">{personality_type}</a>)'
    )


def determine_zodiac_sign(*, month: int, day: int) -> str:
    zodiac_signs = {
        '♈️ Овен': ((3, 21), (4, 19)),
        '♉️ Телец': ((4, 20), (5, 20)),
        '♊️ Близнецы': ((5, 21), (6, 20)),
        '♋️ Рак': ((6, 21), (7, 22)),
        '♌️ Лев': ((7, 23), (8, 22)),
        '♍️ Дева': ((8, 23), (9, 22)),
        '♎️ Весы': ((9, 23), (10, 22)),
        '♏️ Скорпион': ((10, 23), (11, 21)),
        '♐️ Стрелец': ((11, 22), (12, 21)),
        '♑️ Козерог': ((12, 22), (1, 19)),
        '♒️ Водолей': ((1, 20), (2, 18)),
        '♓️ Рыбы': ((2, 19), (3, 20)),
    }

    for sign, (start, end) in zodiac_signs.items():
        start_month, start_day = start
        end_month, end_day = end

        is_born_date_matches = (
                (month == start_month and day >= start_day)
                or (month == end_month and day <= end_day)
        )
        if is_born_date_matches:
            return sign

    return 'Неопеределено'
