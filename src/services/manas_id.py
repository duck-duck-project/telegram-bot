from datetime import date

__all__ = (
    'humanize_personality_type',
    'determine_zodiac_sign',
    'compute_lifetime',
)


def humanize_personality_type(personality_type: str | None) -> str:
    if personality_type is None:
        return 'не указано'

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
        '♈️ Овен': ((3, 21), (4, 20)),
        '♉️ Телец': ((4, 21), (5, 20)),
        '♊️ Близнецы': ((5, 21), (6, 21)),
        '♋️ Рак': ((6, 22), (7, 22)),
        '♌️ Лев': ((7, 23), (8, 23)),
        '♍️ Дева': ((8, 24), (9, 23)),
        '♎️ Весы': ((9, 24), (10, 23)),
        '♏️ Скорпион': ((10, 24), (11, 22)),
        '♐️ Стрелец': ((11, 23), (12, 21)),
        '♑️ Козерог': ((12, 22), (1, 20)),
        '♒️ Водолей': ((1, 21), (2, 20)),
        '♓️ Рыбы': ((2, 21), (3, 20)),
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


def compute_lifetime(born_at: date) -> int:
    today = date.today()
    return (today - born_at).days
