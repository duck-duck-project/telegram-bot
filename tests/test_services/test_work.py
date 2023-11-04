import pytest

from models import ArithmeticExpression
from services.work import ArithmeticProblem


@pytest.mark.parametrize(
    'expression, expected_answer',
    [
        ('6**2*1+7**2*1', 85),
        ('4+12**2-2+41', 187),
        ('3*5+2-1', 16),
        ('9-4*2**2', -7),
        ('10*3**2-5+7', 92),
        ('15-2**3*2', -1),
        ('7*4+6-5**2', 9),
    ]
)
def test_arithmetic_problem_compute_correct_answer(
        expression: str,
        expected_answer: int,
) -> None:
    arithmetic_problem = ArithmeticProblem(ArithmeticExpression(expression))
    assert arithmetic_problem.compute_correct_answer() == expected_answer


@pytest.mark.parametrize(
    'expression, expected_reward_value',
    [
        ('6**2*1+7**2*1', 70),
        ('4+12**2-2+41', 47),
        ('3*5+2-1', 37),
        ('9-4*2**2', 42),
        ('10*3**2-5+7', 52),
        ('15-2**3*2', 57),
        ('7*4+6-5**2', 52),
    ]
)
def test_compute_reward_value(
        expression: str,
        expected_reward_value: int,
) -> None:
    arithmetic_problem = ArithmeticProblem(ArithmeticExpression(expression))
    assert arithmetic_problem.compute_reward_value() == expected_reward_value


if __name__ == '__main__':
    pytest.main()
