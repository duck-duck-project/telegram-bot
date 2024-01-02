from datetime import date

__all__ = ('compute_age',)


def compute_age(born_at: date) -> int:
    today = date.today()
    return today.year - born_at.year - (
        (today.month, today.day) < (born_at.month, born_at.day)
    )
