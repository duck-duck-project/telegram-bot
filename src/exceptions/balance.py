from dataclasses import dataclass

__all__ = (
    'InsufficientFundsForWithdrawalError',
    'InsufficientFundsForTransferError',
    'InsufficientFundsForBetError',
    'TransactionDoesNotExistError',
    'TransferRollbackExpiredError',
    'TransactionDoesNotBelongToUserError',
    'InsufficientFundsForTransferRollbackError',
)


@dataclass(frozen=True, slots=True)
class InsufficientFundsForWithdrawalError(Exception):
    amount: int

    def __str__(self):
        return f'Insufficient funds for withdrawal: {self.amount=}'


class InsufficientFundsForTransferError(Exception):
    pass


class InsufficientFundsForBetError(Exception):
    pass


class TransactionDoesNotExistError(Exception):
    pass


class TransferRollbackExpiredError(Exception):
    pass


class TransactionDoesNotBelongToUserError(Exception):
    pass


class InsufficientFundsForTransferRollbackError(Exception):
    pass
