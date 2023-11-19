import random

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from services import get_random_emoji
from views import ProbabilityAnswerView, reply_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower().startswith('вероятность'),
    StateFilter('*'),
)
async def on_ask_for_probability(message: Message):
    view = ProbabilityAnswerView(
        question=message.text,
        answer_emoji=get_random_emoji(),
        probability=random.randint(0, 100),
    )
    await reply_view(message=message, view=view)
