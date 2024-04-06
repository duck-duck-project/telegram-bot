from dataclasses import dataclass

__all__ = (
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
    'ContactCreateToSelfError',
    'ContactCreateForbiddenError',
)


@dataclass(frozen=True, slots=True)
class ContactDoesNotExistError(Exception):
    contact_id: int

    def __str__(self) -> str:
        return f'Contact with ID {self.contact_id} does not exist'


class ContactAlreadyExistsError(Exception):
    pass


class ContactCreateToSelfError(Exception):
    pass


class ContactCreateForbiddenError(Exception):
    pass
