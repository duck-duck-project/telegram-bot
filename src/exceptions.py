from dataclasses import dataclass


class ServerAPIError(Exception):
    pass


class SecretMessageDoesNotExistError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class UserDoesNotExistError(Exception):
    user_id: int

    def __str__(self):
        return f'User with Telegram ID {self.user_id} does not exist'


@dataclass(frozen=True, slots=True)
class UserAlreadyExistsError(Exception):
    user_id: int

    def __str__(self):
        return f'User with Telegram ID {self.user_id} already exists'


class ContactAlreadyExistsError(Exception):
    pass


class SecretMediaAlreadyExistsError(Exception):
    pass


class SecretMediaDoesNotExistError(Exception):
    pass


class InvalidSecretMediaDeeplinkError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class ContactDoesNotExistError(Exception):
    contact_id: int

    def __str__(self) -> str:
        return f'Contact with ID {self.contact_id} does not exist'


class UserHasNoPremiumSubscriptionError(Exception):
    pass


class ThemeDoesNotExistError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class InsufficientFundsForWithdrawalError(Exception):
    amount: int

    def __str__(self):
        return f'Insufficient funds for withdrawal: {self.amount=}'


class InsufficientFundsForTransferError(Exception):
    pass


class InsufficientFundsForBetError(Exception):
    pass
