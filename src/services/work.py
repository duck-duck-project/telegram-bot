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
    """Returns a random operator sign. Plus, minus or multiply."""
    return random.choice('+-*')


class ArithmeticProblem:

    def __init__(self, expression: ArithmeticExpression):
        self.expression = expression

    def compute_correct_answer(self) -> int:
        """Computes the correct answer for the problem."""
        return eval(self.expression)

    def compute_reward_value(self) -> int:
        """Computes the reward value for solving the problem."""
        operators_complexity_value = (
                self.expression.count('+') * 3
                + self.expression.count('-') * 5
                + self.expression.count('*') * 5
        )
        answer_complexity = abs(self.compute_correct_answer()) // 10
        return operators_complexity_value + answer_complexity

    @classmethod
    def from_text(cls, text: str) -> Self:
        """
        Returns an arithmetic problem from a text.

        Args:
            text: The text to parse the arithmetic problem from.

        Returns:
            An arithmetic problem.
        """
        expression = ArithmeticExpression(
            text.split('\n')[0]
            .removeprefix('❓ Сколько будет: ')
            .removesuffix('?')
        )
        return cls(expression=expression)


def get_arithmetic_expression() -> ArithmeticExpression:
    """Returns an arithmetic expression with random operators and operands."""
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
    """Returns an arithmetic problem with a random expression."""
    expression = get_arithmetic_expression()
    return ArithmeticProblem(expression)


def compute_final_reward(
        *,
        reward_value: int,
        premium_multiplier: int | float,
        is_premium: bool,
) -> int:
    """
    Computes the final reward value based on the premium status of the user.

    Keyword Args:
        reward_value: The reward value to compute.
        premium_multiplier: The multiplier to apply to the reward value if the
            user is premium.
        is_premium: Whether the user is premium or not.

    Returns:
        The final reward value.
    """
    if is_premium:
        return reward_value * premium_multiplier
    return int(reward_value)
