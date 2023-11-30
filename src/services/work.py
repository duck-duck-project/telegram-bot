import random
from dataclasses import dataclass
from typing import Self

from models import ArithmeticExpression, HumanizedArithmeticExpression

__all__ = (
    'ArithmeticProblem',
    'get_arithmetic_problem',
    'get_random_operator',
    'get_arithmetic_expression',
)


@dataclass(frozen=True, slots=True)
class ArithmeticProblem:
    expression: ArithmeticExpression

    def __str__(self):
        return self.get_humanized_expression()

    def get_humanized_expression(self) -> HumanizedArithmeticExpression:
        """Returns a humanized arithmetic expression."""
        humanized_arithmetic_expression = self.expression.replace('**2', '²')
        return HumanizedArithmeticExpression(humanized_arithmetic_expression)

    def compute_correct_answer(self) -> int:
        """Computes the correct answer for the problem."""
        return eval(self.expression)

    def compute_reward_value(self) -> int:
        """Computes the reward value for solving the problem."""
        humanized_expression = self.get_humanized_expression()
        return (
                humanized_expression.count('+') * 23
                + humanized_expression.count('-') * 26
                + humanized_expression.count('*') * 30
                + humanized_expression.count('²') * 35
        )

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
            .replace('²', '**2')
        )
        return cls(expression=expression)


def get_square_or_empty_string() -> str:
    """
    Returns a square sign or an empty string. Change to ² with 1/5 probability.

    Returns:
        A square sign or an empty string.
    """
    return '**2' if random.randint(0, 4) == 0 else ''


def get_random_operator() -> str:
    """
    Returns a random operator sign. Plus, minus or multiply.

    Returns:
        A random operator sign (+, - or *).
    """
    return random.choice('+-*')


def get_arithmetic_expression() -> ArithmeticExpression:
    """Returns an arithmetic expression with random operators and operands."""
    expression = (
        f'{get_random_operator()}'
        f'{random.randint(1, 9)}'
        f'{get_square_or_empty_string()}'
        f'{get_random_operator()}'
        f'{random.randint(1, 9)}'
        f'{get_square_or_empty_string()}'
        f'{get_random_operator()}'
        f'{random.randint(1, 9)}'
        f'{get_square_or_empty_string()}'
        f'{get_random_operator()}'
        f'{random.randint(1, 9)}'
        f'{get_square_or_empty_string()}'
    ).lstrip('+*')
    return ArithmeticExpression(expression)


def get_arithmetic_problem() -> ArithmeticProblem:
    """Returns an arithmetic problem with a random expression."""
    expression = get_arithmetic_expression()
    return ArithmeticProblem(expression)
