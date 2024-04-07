from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from enums import TruthOrDareQuestionType
from filters import truth_or_dare_question_filter
from repositories import QuizRepository

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower() == 'пожелание',
    StateFilter('*'),
)
async def on_show_wish(
        message: Message,
        quiz_repository: QuizRepository,
) -> None:
    wish = await quiz_repository.get_random_wish()
    if wish is None:
        await message.answer('Не могу пока ничего пожелать 😔')
    else:
        await message.reply(wish)


@router.message(
    F.text.lower() == 'предсказание',
    StateFilter('*'),
)
async def on_show_prediction(
        message: Message,
        quiz_repository: QuizRepository,
) -> None:
    wish = await quiz_repository.get_random_prediction()
    if wish is None:
        await message.answer('Не могу дать вам предсказание 😔')
    else:
        await message.reply(wish)


@router.message(
    truth_or_dare_question_filter,
    StateFilter('*'),
)
async def on_show_truth_or_dare_question(
        message: Message,
        quiz_repository: QuizRepository,
        question_type: TruthOrDareQuestionType | None,
) -> None:
    question = await quiz_repository.get_random_truth_or_dare_question(
        question_type=question_type
    )
    if question is None:
        await message.answer('Не могу дать вам вопрос 😔')
    else:
        await message.reply(question)
