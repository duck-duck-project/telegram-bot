import random

__all__ = ('COOL_EMOJIS', 'get_random_emoji')

COOL_EMOJIS = (
    "😎",
    "🤓",
    "🤩",
    "🥳",
    "🤯",
    "🤪",
    "🤑",
    "🤠",
    "🥸",
    "🤗",
    "🤔",
    "🤨",
    "🧐",
    "🤫",
    "🤭",
    "🤥",
    "🤐",
    "🤧",
    "🥵",
    "🥶",
    "🥴",
    "😵",
)


def get_random_emoji() -> str:
    return random.choice(COOL_EMOJIS)
