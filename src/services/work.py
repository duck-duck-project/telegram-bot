import random
from typing import Self

from models import ArithmeticExpression

__all__ = (
    'ArithmeticProblem',
    'get_arithmetic_problem',
    'get_operator_sign',
    'get_arithmetic_expression',
    'compute_final_reward',
)


def get_operator_sign() -> str:
    return random.choice('+-*')


class ArithmeticProblem:

    def __init__(self, expression: ArithmeticExpression):
        self.expression = expression

    def compute_correct_answer(self) -> int:
        return eval(self.expression)

    def compute_reward_value(self) -> int:
        operators_complexity_value = (
                self.expression.count('+') * 3
                + self.expression.count('-') * 5
                + self.expression.count('*') * 5
        )
        answer_complexity = abs(self.compute_correct_answer()) // 10
        return operators_complexity_value + answer_complexity

    @classmethod
    def from_text(cls, text: str) -> Self:
        expression = ArithmeticExpression(
            text.split('\n')[0]
            .removeprefix('❓ Сколько будет: ')
            .removesuffix('?')
        )
        return cls(expression=expression)


def get_arithmetic_expression() -> ArithmeticExpression:
    expression = (
        f'{get_operator_sign()}'
        f'{random.randint(1, 10)}'
        f'{get_operator_sign()}'
        f'{random.randint(1, 10)}'
        f'{get_operator_sign()}'
        f'{random.randint(1, 10)}'
        f'{get_operator_sign()}'
        f'{random.randint(1, 10)}'
    ).lstrip('+*')
    return ArithmeticExpression(expression)


def get_arithmetic_problem() -> ArithmeticProblem:
    expression = get_arithmetic_expression()
    return ArithmeticProblem(expression)


def compute_final_reward(
        *,
        reward_value: int,
        premium_multiplier: int | float,
        is_premium: bool,
) -> int:
    if is_premium:
        return reward_value * premium_multiplier
    return int(reward_value)
