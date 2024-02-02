from datetime import date

__all__ = ('compute_age', 'compute_days_until_birthday')


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
