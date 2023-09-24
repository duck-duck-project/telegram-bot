from typing import NewType

from pydantic import BaseModel

__all__ = (
    'ArithmeticExpression',
    'ArithmeticProblem',
)

ArithmeticExpression = NewType('ArithmeticExpression', str)


class ArithmeticProblem(BaseModel):
    expression: ArithmeticExpression
    correct_answer: int
