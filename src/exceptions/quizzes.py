from exceptions.base import ApplicationError

__all__ = (
    'WishNotFoundError',
    'PredictionNotFoundError',
    'TruthOrDareQuestionNotFoundError',
)


class WishNotFoundError(ApplicationError):
    pass


class PredictionNotFoundError(ApplicationError):
    pass


class TruthOrDareQuestionNotFoundError(ApplicationError):
    pass
