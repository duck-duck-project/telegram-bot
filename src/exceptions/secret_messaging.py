from exceptions.base import ApplicationError

__all__ = (
    'SecretMessageDoesNotExistError',
    'SecretMediaDoesNotExistError',
    'SecretMediaAlreadyExistsError',
    'InvalidSecretMediaDeeplinkError',
)


class SecretMessageDoesNotExistError(ApplicationError):
    pass


class SecretMediaAlreadyExistsError(ApplicationError):
    pass


class SecretMediaDoesNotExistError(ApplicationError):
    pass


class InvalidSecretMediaDeeplinkError(ApplicationError):
    pass
