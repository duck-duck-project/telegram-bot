from typing import NewType

__all__ = ('ArithmeticExpression', 'HumanizedArithmeticExpression')

ArithmeticExpression = NewType('ArithmeticExpression', str)
HumanizedArithmeticExpression = NewType('HumanizedArithmeticExpression', str)
