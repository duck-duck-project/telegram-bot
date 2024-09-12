from exceptions.base import ApplicationError

__all__ = (
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
    'ContactCreateToSelfError',
    'ContactCreateForbiddenError',
)


class ContactDoesNotExistError(ApplicationError):

    def __init__(self, detail: str, contact_id: int):
        super().__init__(detail)
        self.contact_id = contact_id


class ContactAlreadyExistsError(ApplicationError):
    pass


class ContactCreateToSelfError(ApplicationError):
    pass


class ContactCreateForbiddenError(ApplicationError):
    pass
