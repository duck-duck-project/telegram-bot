from exceptions.base import ApplicationError

__all__ = (
    'TagNotFoundError',
    'TagDoesNotBelongToUserError',
)


class TagNotFoundError(ApplicationError):
    pass


class TagDoesNotBelongToUserError(ApplicationError):
    pass
