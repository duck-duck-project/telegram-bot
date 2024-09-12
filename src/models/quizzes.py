from pydantic import BaseModel

from enums import TruthOrDareQuestionType

__all__ = ('Wish', 'Prediction', 'TruthOrDareQuestion')


class Wish(BaseModel):
    text: str


class Prediction(BaseModel):
    text: str


class TruthOrDareQuestion(BaseModel):
    text: str
    type: TruthOrDareQuestionType
