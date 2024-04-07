from aiogram.types import Message

from enums import TruthOrDareQuestionType

__all__ = ('truth_or_dare_question_filter',)


def truth_or_dare_question_filter(message: Message) -> dict | bool:
    if message.text is None:
        return False

    if message.text.lower() == 'правда':
        return {'question_type': TruthOrDareQuestionType.TRUTH}

    if message.text.lower() == 'действие':
        return {'question_type': TruthOrDareQuestionType.DARE}

    if message.text.lower() in {'правда или действие', 'пд'}:
        return {'question_type': None}

    return False
