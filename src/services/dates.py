from datetime import date

__all__ = (
    'compute_age',
    'compute_days_until_birthday',
    'humanize_age',
)


def humanize_age(born_on: date) -> str:
    age = compute_age(born_on)

    is_last_digit_between_1_and_4 = 4 >= age % 10 >= 1
    is_age_not_10 = age // 10 != 1
    if is_last_digit_between_1_and_4 and is_age_not_10:
        age_suffix = 'года'
    else:
        age_suffix = 'лет'

    return f'{age} {age_suffix}'


def compute_age(born_at: date) -> int:
    today = date.today()
    return today.year - born_at.year - (
            (today.month, today.day) < (born_at.month, born_at.day)
    )


def compute_days_until_birthday(now: date, born_at: date) -> int:
    birthday = born_at.replace(year=now.year)
    if birthday < now:
        birthday = birthday.replace(year=now.year + 1)
    return (birthday - now).days
