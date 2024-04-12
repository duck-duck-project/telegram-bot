__all__ = (
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
    'ContactCreateToSelfError',
    'ContactCreateForbiddenError',
)


class ContactDoesNotExistError(Exception):

    def __init__(self, contact_id: int):
        self.contact_id = contact_id

    def __str__(self) -> str:
        return f'Contact with ID {self.contact_id} does not exist'


class ContactAlreadyExistsError(Exception):
    pass


class ContactCreateToSelfError(Exception):
    pass


class ContactCreateForbiddenError(Exception):
    pass
